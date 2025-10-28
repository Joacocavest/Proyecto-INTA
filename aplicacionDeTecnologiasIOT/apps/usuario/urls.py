from django.urls import path
from apps.usuario import views

app_name = 'usuario'
urlpatterns = [
    path('index/', views.index, name="index"),
    path('registrar/', views.registrar_usuario, name="registrar_usuario"),
    path("iniciar-sesion/", views.iniciar_sesion, name="iniciar_sesion"),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path('home/', views.home, name='home'),
    
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuario/<int:pk>/', views.usuario, name='usuario'),
    
    path('cuidadores/', views.lista_cuidadores, name='lista_cuidadores'),
    path('cuidador/<int:pk>/', views.cuidador, name='cuidador'),
    
    path('crear_establecimiento/', views.crear_establecimiento, name='crear_establecimiento'),
    path('establecimientos/', views.lista_establecimientos, name='lista_establecimientos'),
    path('establecimiento/<str:pk>/', views.establecimiento, name='establecimiento'),
    path('buscar_establecimiento/', views.buscar_establecimiento, name='buscar_establecimiento'),
    path("listar_auxiliares/", views.listar_establecimientos_auxiliares, name="listar_auxiliares"),
    
    path('roles/', views.lista_roles, name='lista_roles'),
    path('rol/<int:pk>/', views.rol, name='rol')
]
 