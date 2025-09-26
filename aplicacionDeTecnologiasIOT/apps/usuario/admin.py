from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, Establecimiento, Cuidador
from .forms import UsuarioCreationForm, UsuarioChangeForm

class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    model = Usuario
    
    # Campos que se muestran en el listado de usuarios
    list_display = ['username', 'email', 'CUIT', 'nombre', 'apellido', 'telefono', 'is_staff']

    # Campos visibles al editar un usuario
    fieldsets = (
        (None, {'fields': ('username', 'contraseña')}),  
        ('Información personal', {'fields': ('nombre', 'apellido', 'email', 'telefono', 'CUIG', 'id_rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Campos visibles al crear un usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'CUIT', 'nombre', 'apellido', 'email', 'telefono', 'CUIG', 'id_rol', 'contraseña'),
        }),
    )

    search_fields = ('username', 'CUIT','email', 'nombre', 'apellido')
    ordering = ('username', 'CUIT')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol)
admin.site.register(Establecimiento)
admin.site.register(Cuidador)