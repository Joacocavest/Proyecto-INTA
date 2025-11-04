from django.shortcuts import get_object_or_404, redirect, render
from apps.usuario.models import Usuario, Cuidador, Establecimiento, Rol, SolicitudUnion
from apps.usuario.forms import UsuarioRegistroForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Max, IntegerField
from django.db.models.functions import Substr, Cast
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def index(request):
    return render(request, "base/index.html")

def home(request):
    return render(request, "usuario/home.html")

#VISTA PARA REGISTRAR UN USUARIO#
def registrar_usuario(request):
    if request.method == "POST":
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.id_rol = None      # Sin rol aún
            user.CUIG = None        # Sin establecimiento aun
            user.save()

            messages.info(request, "Usuario registrado correctamente, ahora inicia sesión")
            return redirect("usuario:iniciar_sesion")
        else:
            print(form.errors)
    else:
        form = UsuarioRegistroForm()
    return render(request, "usuario/registrar_usuario.html", {"form": form})


#VISTA PARA INICIAR SESION
def iniciar_sesion(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido {user.nombre} 👋")
            return redirect("usuario:home") #redirige al home
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, "usuario/iniciar_sesion.html")

#VISTA PARA CERRAR SESION
@login_required
def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Cerraste sesión correctamente.")
    return redirect("index")


#VISTA PARA LISTAR LOS USUARIOS#
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuario/lista_usuarios.html', {'usuarios':usuarios})

#VISTA PARA VER UN USUARIO
def usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'usuario/usuario.html', {'usuario':usuario})


#VISTA PARA LISTAR LOS CUIDADORES#
def lista_cuidadores(request):
    cuidadores = Cuidador.objects.all()
    return render(request, 'cuidador/lista_cuidadores.html', {'cuidadores': cuidadores})

#VISTA PARA VER UN CUIDADOR
def cuidador(request, pk):
    cuidador = get_object_or_404(Cuidador, pk=pk)
    return render(request, 'cuidador/cuidador.html', {'cuidador':cuidador})










# VISTA PARA CREAR UN ESTABLECIMIENTO PARTICULAR
@login_required
def crear_establecimiento(request):
    # Si el usuario ya tiene CUIG, no debería volver a crear uno
    if request.user.CUIG:
        messages.warning(request, "Ya perteneces a un establecimiento.")
        return redirect("usuario:home")

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        provincia = request.POST.get("provincia")
        departamento = request.POST.get("departamento")
        localidad = request.POST.get("localidad")
        direccion = request.POST.get("direccion")

        #1 Generar un nuevo CUIG único
        ultimo_establecimiento = Establecimiento.objects.filter(CUIG__startswith="AUX").order_by("-CUIG").first()

        if ultimo_establecimiento:
            # Extraer número de CUIG (ej: "AUX0002" → 2)
            ultimo_numero = int(ultimo_establecimiento.CUIG.replace("AUX", ""))
            nuevo_numero = ultimo_numero + 1
        else:
            nuevo_numero = 1  # Si no hay ninguno aún

        nuevo_CUIG = f"AUX{nuevo_numero:04d}"

        # 2 Crear el establecimiento
        establecimiento = Establecimiento.objects.create(
            CUIG=nuevo_CUIG,
            nombre=nombre,
            provincia=provincia,
            departamento=departamento,
            localidad=localidad,
            direccion=direccion,
            creado_por=request.user
        )

        # 3 Asignar el CUIG y el rol de Administrador al usuario creador
        rol_admin = Rol.objects.get(nombre_rol="Administrador")
        request.user.CUIG = establecimiento
        request.user.id_rol = rol_admin
        request.user.save()

        # 4 Confirmar éxito
        messages.success(request, f"Establecimiento '{nombre}' creado exitosamente con CUIG {nuevo_CUIG}.")
        return redirect("usuario:home")

    # 5 Si no es POST, mostrar el formulario
    return render(request, "usuario/crear_establecimiento.html")



# VISTA PARA UNIRSE A UN ESTABLECIMIENTO
@login_required
def unirse_establecimiento(request):
    tipo = request.GET.get("tipo")
    establecimientos = Establecimiento.objects.all()

    # Filtrado opcional
    if tipo == "particular":
        establecimientos = establecimientos.filter(CUIG__startswith="AUX")
    elif tipo == "senasa":
        establecimientos = establecimientos.exclude(CUIG__startswith="AUX")

    if request.method == "POST":
        cuig = request.POST.get("establecimiento_id")
        rol_id = request.POST.get("rol_id")  # si más adelante agregás roles específicos

        # Buscar por CUIG
        establecimiento = get_object_or_404(Establecimiento, CUIG=cuig)
        rol = Rol.objects.get(id=rol_id) if rol_id else None

        # Evitar solicitudes duplicadas
        if SolicitudUnion.objects.filter(usuario=request.user, establecimiento=establecimiento, estado="Pendiente").exists():
            messages.warning(request, "Ya enviaste una solicitud pendiente a este establecimiento.")
            return redirect("usuario:unirse_establecimiento")

        # Crear solicitud
        SolicitudUnion.objects.create(
            usuario=request.user,
            establecimiento=establecimiento,
        )

        messages.success(request, f"Solicitud enviada al establecimiento '{establecimiento.nombre}'.")
        return redirect("usuario:home")

    return render(request, "usuario/unirse_establecimiento.html", {
        "establecimientos": establecimientos
    })



# VISTA PARA VER LAS SOLICITUDES DE UNION A UN ESTABLECIMIENTO
@login_required
def ver_solicitudes_union(request):
    # 1. Validar que el usuario sea Administrador con CUIG
    if not request.user.CUIG or request.user.id_rol.nombre_rol != "Administrador":
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect("usuario:home")

    # 2. Solicitudes pendientes
    solicitudes = SolicitudUnion.objects.filter(
        establecimiento=request.user.CUIG,
        estado="Pendiente"
    )

    # 3. Traer roles disponibles (excepto administrador)
    roles_disponibles = Rol.objects.all()

    # 4. Procesar aprobación/rechazo
    if request.method == "POST":
        solicitud_id = request.POST.get("solicitud_id")
        accion = request.POST.get("accion")
        rol_id = request.POST.get("rol_id")

        solicitud = get_object_or_404(SolicitudUnion, id=solicitud_id)

        if solicitud.establecimiento != request.user.CUIG:
            messages.error(request, "No puedes gestionar solicitudes de otro establecimiento.")
            return redirect("usuario:ver_solicitudes_union")

        if accion == "aprobar":
            if not rol_id:
                messages.warning(request, "Debes seleccionar un rol antes de aprobar.")
                return redirect("usuario:ver_solicitudes_union")

            rol = get_object_or_404(Rol, id=rol_id)
            solicitud.estado = "Aprobada"
            solicitud.usuario.CUIG = solicitud.establecimiento
            solicitud.usuario.id_rol = rol
            solicitud.usuario.save()
            messages.success(request, f"Solicitud aprobada para {solicitud.usuario.username} con rol {rol.nombre_rol}.")
        
        elif accion == "rechazar":
            solicitud.estado = "Rechazada"
            messages.info(request, f"Solicitud rechazada para {solicitud.usuario.username}.")

        solicitud.revisado_por = request.user
        solicitud.fecha_revision = timezone.now()
        solicitud.save()

        return redirect("usuario:ver_solicitudes_union")

    # 5. Renderizar
    return render(request, "usuario/ver_solicitudes_union.html", {
        "solicitudes": solicitudes,
        "roles": roles_disponibles
    })




#VISTA PARA LISTAR LOS ESTABLECIMIENTOS#
def lista_establecimientos(request):
    establecimientos = Establecimiento.objects.all()
    return render(request, 'establecimiento/lista_establecimientos.html', {'establecimientos':establecimientos})

#VISTA PARA VER UN ESTABLECIMIENTO
def establecimiento(request, pk):
    establecimiento = get_object_or_404(Establecimiento, pk=pk)
    return render(request, 'establecimiento/establecimiento.html', {'establecimiento':establecimiento})


def buscar_establecimiento(request):
    """
    Endpoint AJAX: busca un establecimiento por CUIG y devuelve sus datos en JSON.
    """
    cuig = request.GET.get("CUIG")
    if not cuig:
        return JsonResponse({"error": "CUIG no proporcionado"}, status=400)

    try:
        establecimiento = Establecimiento.objects.get(CUIG=cuig)
        data = {
            "existe": True,
            "nombre": establecimiento.nombre,
            "provincia": establecimiento.provincia,
            "departamento": establecimiento.departamento,
            "localidad": establecimiento.localidad,
            "direccion": establecimiento.direccion,
            "logo": establecimiento.logo.url if establecimiento.logo else None,
        }
    except Establecimiento.DoesNotExist:
        data = {"existe": False}

    return JsonResponse(data)


#VISTA PARA ESTABLECIMIENTOS PARTICULARES NO RECONOCIDOS POR EL SENASA
def listar_establecimientos_auxiliares(request):
    auxiliares = Establecimiento.objects.filter(CUIG__startswith="AUX").values("CUIG", "nombre")
    return JsonResponse(list(auxiliares), safe=False)


#VISTA PARA LISTAR LOS ROLES#
def lista_roles(request):
    roles = Rol.objects.all()
    return render(request, 'rol/lista_roles.html', {'roles':roles})

#VISTA PARA VER UN ROL
def rol(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    return render(request, 'rol/rol.html', {'rol':rol})