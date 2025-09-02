from django.urls import path
from apps.usuario import views

app_name = 'usuario'
urlpatterns = [
    path('', views.lista_usuarios, name='lista_usuarios'),
    path('<int:pk>', views.usuario, name='usuario'),
    path('', views.lista_cuidadores, name='lista_cuidadores'),
    path('<int:pk>', views.cuidador, name='cuidador'),
    path('', views.lista_establecimientos, name='lista_establecimientos'),
    path('<int:pk>', views.establecimiento, name='establecimiento'),
    path('', views.lista_roles, name='lista_roles'),
    path('<int:pk>', views.rol, name='rol')
]
 