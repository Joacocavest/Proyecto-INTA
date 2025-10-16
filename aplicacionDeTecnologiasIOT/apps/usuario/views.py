from django.shortcuts import get_object_or_404, redirect, render
from apps.usuario.models import Usuario, Cuidador, Establecimiento, Rol
from apps.usuario.forms import UsuarioRegistroForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Max, IntegerField
from django.db.models.functions import Substr, Cast
import re

def index(request):
    return render(request, "base/index.html")

def home(request):
    return render(request, "usuario/home.html")

#VISTA PARA REGISTRAR UN USUARIO#
def registrar_usuario(request):
    if request.method == "POST":
        form = UsuarioRegistroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado correctamente")
            return redirect("index")  #vuelve a inicio después de registrar
        else:
            print(form.errors)
    else:
        form = UsuarioRegistroForm()
    return render(request, "usuario/registrar_usuario.html", {"form": form})



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



# VISTA PARA CREAR ESTABLECIMIENTO PARTICULAR NO RECONOCIDO POR EL SENASA
def crear_establecimiento_auxiliar(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()

        if not nombre:
            return JsonResponse({"error": "Debe indicar un nombre para el establecimiento."}, status=400)

        # Buscar el número máximo actual (parte numérica del CUIG)
        ultimo = (
            Establecimiento.objects
            .filter(CUIG__startswith="AUX")
            .annotate(num_part=Cast(Substr("CUIG", 4), IntegerField()))
            .aggregate(max_num=Max("num_part"))
            .get("max_num")
        )

        # Calcular el siguiente CUIG disponible
        next_num = (ultimo or 0) + 1
        nuevo_cuig = f"AUX{next_num:04d}"

        # Crear el nuevo establecimiento auxiliar
        establecimiento_aux = Establecimiento.objects.create(
            CUIG=nuevo_cuig,
            nombre=nombre
        )

        return JsonResponse({
            "success": True,
            "CUIG": establecimiento_aux.CUIG,
            "nombre": establecimiento_aux.nombre
        })

    #Si no es POST, devolver error
    return JsonResponse({"error": "Método no permitido."}, status=405)

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