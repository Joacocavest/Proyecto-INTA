from django.contrib import admin
from .models import Usuario, Cuidador, Rol, Establecimiento

@admin.register(Establecimiento)
class EstablecimientoAdmin(admin.ModelAdmin):
    list_display = ('CUIG', 'nombre', 'provincia', 'departamento', 'localidad')
    search_fields = ('CUIG', 'nombre', 'provincia', 'localidad')
    list_filter = ('provincia', 'departamento')
    fields = ('CUIG', 'nombre', 'provincia', 'departamento', 'localidad', 'direccion', 'logo')

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_rol', 'descripcion_rol')
    search_fields = ('nombre_rol',)
    fields = ('nombre_rol', 'descripcion_rol')

@admin.register(Cuidador)
class CuidadorAdmin(admin.ModelAdmin):
    list_display = ('CUIT', 'nombre_cuidador', 'apellido_cuidador', 'CUIG', 'sector', 'email')
    list_filter = ('CUIG', 'sector')
    search_fields = ('nombre_cuidador', 'apellido_cuidador', 'CUIT', 'email')
    fields = ('CUIT', 'CUIG', 'sector', 'nombre_cuidador', 'apellido_cuidador', 'email', 'telefono')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'nombre', 'apellido', 'CUIG', 'id_rol', 'email', 'is_active')
    list_filter = ('id_rol', 'CUIG', 'is_active')
    search_fields = ('nombre', 'apellido', 'username', 'email')
    fields = ('username', 'password', 'nombre', 'apellido', 'nombre_usuario', 'contraseña', 
              'email', 'telefono', 'CUIG', 'id_rol', 'is_active', 'is_staff')
