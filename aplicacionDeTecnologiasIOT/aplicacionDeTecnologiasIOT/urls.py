"""
URL configuration for aplicacionDeTecnologiasIOT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.usuario import views as usuario_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', usuario_views.home, name='home'),
    #vistas de usuario, cuidador, establecimiento y rol:
    path('usuario/', include('apps.usuario.urls', namespace='usuario')),
    
    #vistas de nodo y lectura:
    path('nodo/', include('apps.nodos.urls', namespace='nodo')),
    
    #vistas de animal, especie y raza
    path('animal/', include('apps.animal.urls', namespace='animal'))
]

if settings.DEBUG:  # Solo en modo desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
