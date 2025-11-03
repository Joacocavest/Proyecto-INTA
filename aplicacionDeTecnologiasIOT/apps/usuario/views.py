from django.shortcuts import get_object_or_404, redirect, render
from apps.usuario.models import Usuario, Cuidador, Establecimiento, Rol
from apps.usuario.forms import UsuarioRegistroForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Max, IntegerField
from django.db.models.functions import Substr, Cast
from django.contrib.auth.decorators import login_required

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




#VISTA PARA SOLICITAR ESTABLECIMIENTO
# @login_required
# def solicitud_establecimiento(request):
#     usuario = request.user

#     # Solo usuarios pendientes pueden crear una solicitud
#     if usuario.estado != "pendiente":
#         messages.warning(request, "Ya tienes un establecimiento o no estás autorizado para crear una nueva solicitud.")
#         return redirect("index")

#     if request.method == "POST":
#         form = SolicitudEstablecimientoForm(request.POST)
#         if form.is_valid():
#             solicitud = form.save(commit=False)
#             solicitud.usuario = usuario
#             solicitud.estado = "pendiente"
#             solicitud.save()

#             messages.success(request, "Tu solicitud fue enviada y está pendiente de revisión.")
#             return redirect("index")
#     else:
#         form = SolicitudEstablecimientoForm()

#     return render(request, "establecimiento/solicitud_establecimiento.html", {"form": form})


# #VISTA PARA APROBAR SOLICITUD
# @user_passes_test(lambda u: u.is_superuser)
# def aprobar_solicitud(request, solicitud_id):
#     solicitud = get_object_or_404(SolicitudEstablecimiento, pk=solicitud_id)
#     usuario = solicitud.usuario

#     # Crear el establecimiento
#     establecimiento = Establecimiento.objects.create(
#         CUIG=f"AUX{Establecimiento.objects.count()+1:04d}",
#         nombre=solicitud.nombre_establecimiento,
#         provincia=solicitud.provincia,
#         departamento=solicitud.departamento,
#         localidad=solicitud.localidad,
#         direccion=solicitud.direccion,
#         creado_por=usuario
#     )

#     # Activar usuario y asignarle rol admin
#     usuario.CUIG = establecimiento
#     usuario.is_active = True
#     usuario.estado = "Activo"
#     rol_admin = Rol.objects.get(nombre_rol="Administrador")
#     usuario.id_rol = rol_admin
#     usuario.save()

#     solicitud.estado = "Aprobada"
#     solicitud.save()

#     messages.success(request, f"Solicitud aprobada. Establecimiento {establecimiento.nombre} creado.")
#     return redirect("admin:index")



# #VISTA PARA INVITAR USUARIO
# @login_required
# def invitar_usuario(request):
#     usuario = request.user

#     # 🔒 Solo los administradores pueden invitar
#     if usuario.id_rol.nombre != "Administrador":
#         messages.error(request, "No tenés permiso para invitar usuarios.")
#         return redirect("usuario:home")

#     if request.method == "POST":
#         form = InvitacionUsuarioForm(request.POST, establecimiento=usuario.CUIG, invitado_por=usuario)
#         if form.is_valid():
#             invitacion = form.save()
#             messages.success(request, f"Invitación enviada a {invitacion.email}.")
#             return redirect("usuario:home")
#     else:
#         form = InvitacionUsuarioForm()

#     return render(request, "usuario/invitar_usuario.html", {"form": form})



# #VISTA PARA ACEPTAR INFORMACION
# def aceptar_invitacion(request, token):
#     invitacion = get_object_or_404(InvitacionUsuario, token=token, estado="pendiente")

#     if request.method == "POST":
#         password = request.POST.get("password")
#         usuario = Usuario.objects.create_user(
#             username=invitacion.email,
#             email=invitacion.email,
#             password=password,
#             nombre="",
#             apellido="",
#             CUIT=0,
#         )
#         invitacion.aceptar(usuario)
#         messages.success(request, "Invitación aceptada. Ya podés iniciar sesión.")
#         return redirect("usuario:iniciar_sesion")

#     return render(request, "usuario/aceptar_invitacion.html", {"invitacion": invitacion})





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



# # VISTA PARA CREAR ESTABLECIMIENTO PARTICULAR NO RECONOCIDO POR EL SENASA
# def crear_establecimiento_auxiliar(request):
#     if request.method == "POST":
#         nombre = request.POST.get("nombre", "").strip()

#         if not nombre:
#             return JsonResponse({"error": "Debe indicar un nombre para el establecimiento."}, status=400)

#         # Buscar el número máximo actual (parte numérica del CUIG)
#         ultimo = (
#             Establecimiento.objects
#             .filter(CUIG__startswith="AUX")
#             .annotate(num_part=Cast(Substr("CUIG", 4), IntegerField()))
#             .aggregate(max_num=Max("num_part"))
#             .get("max_num")
#         )

#         # Calcular el siguiente CUIG disponible
#         next_num = (ultimo or 0) + 1
#         nuevo_cuig = f"AUX{next_num:04d}"

#         # Crear el nuevo establecimiento auxiliar
#         establecimiento_aux = Establecimiento.objects.create(
#             CUIG=nuevo_cuig,
#             nombre=nombre
#         )

#         return JsonResponse({
#             "success": True,
#             "CUIG": establecimiento_aux.CUIG,
#             "nombre": establecimiento_aux.nombre
#         })

#     #Si no es POST, devolver error
#     return JsonResponse({"error": "Método no permitido."}, status=405)



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