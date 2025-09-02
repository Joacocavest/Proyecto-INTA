from django.urls import path
from apps.nodos import views

app_name = 'nodos'
urlpatterns = [
    path('', views.lista_nodos, name='lista_nodos'),
    path('<int:pk>', views.nodo, name='nodo'),
    path('', views.lista_lecturas, name='lista_lecturas'),
    path('<int:pk>', views.lectura, name='lectura')
]
 