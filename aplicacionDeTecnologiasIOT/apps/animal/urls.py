from django.urls import path
from apps.animal import views

app_name = 'animal'
urlpatterns = [
    path('', views.lista_animales, name='lista_animales'),
    path('<int:pk>', views.animal, name='animal'),
    path('', views.lista_especies, name='lista_especies'),
    path('<int:pk>', views.especie, name='especie'),
    path('', views.lista_razas, name='lista_razas'),
    path('<int:pk>', views.raza, name='raza'),
]