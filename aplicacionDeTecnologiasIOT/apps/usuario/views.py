from django.shortcuts import get_object_or_404, render
from apps.usuario.models import Usuario, Cuidador, Establecimiento, Rol

def home(request):
    return render(request, "base/home.html")


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



#VISTA PARA LISTAR LOS ROLES#
def lista_roles(request):
    roles = Rol.objects.all()
    return render(request, 'rol/lista_roles.html', {'roles':roles})

#VISTA PARA VER UN ROL
def rol(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    return render(request, 'rol/rol.html', {'rol':rol})