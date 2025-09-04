from django.urls import path
from apps.nodos import views

app_name = 'nodos'
urlpatterns = [
    path('lista_nodos/', views.lista_nodos, name='lista_nodos'),
    
    path("form/", views.nodo_form, name="crear_nodo"),          
    path("form/<str:pk>/", views.nodo_form, name="modificar_nodo"),
    
    path('eliminar/<str:pk>/', views.eliminar_nodo, name='eliminar_nodo'),
    
    path('<str:pk>', views.nodo, name='detalle_nodo'),
    
    path('lista_lecturas/', views.lista_lecturas, name='lista_lecturas'),
    path('lectura_nodo/<str:pk>', views.lectura, name='lectura')
]