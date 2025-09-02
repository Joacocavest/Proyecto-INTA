from django.urls import path
from apps.nodos import views

app_name = 'nodos'
urlpatterns = [
    path('agregar_nodo/', views.crear_nodo, name='crear_nodo'),
    path('modificar/<str:pk>/', views.modificar_nodo, name='modificar_nodo'),
    path('eliminar/<str:pk>/', views.eliminar_nodo, name='eliminar_nodo'),
    path('lista_nodos/', views.lista_nodos, name='lista_nodos'),
    path('<int:pk>', views.nodo, name='nodo'),
    path('lista_lecturas/', views.lista_lecturas, name='lista_lecturas'),
    path('lectura_nodo/<int:pk>', views.lectura, name='lectura')
]