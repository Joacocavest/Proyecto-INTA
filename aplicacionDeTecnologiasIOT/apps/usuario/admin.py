from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario 
from .forms import UsuarioCreationForm, UsuarioChangeForm

class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    model = Usuario
    
    # Campos que se muestran en el listado de usuarios
    list_display = ['nombre_usuario', 'email', 'nombre', 'apellido', 'telefono', 'is_staff']

    # Campos visibles al editar un usuario
    fieldsets = (
        (None, {'fields': ('nombre_usuario', 'contraseña')}),  
        ('Información personal', {'fields': ('nombre', 'apellido', 'email', 'telefono', 'CUIG', 'id_rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Campos visibles al crear un usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre_usuario', 'nombre', 'apellido', 'email', 'telefono', 'CUIG', 'id_rol', 'contraseña'),
        }),
    )

    search_fields = ('nombre_usuario', 'email', 'nombre', 'apellido')
    ordering = ('nombre_usuario',)

admin.site.register(Usuario, UsuarioAdmin)
