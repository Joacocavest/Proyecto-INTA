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
        (None, {'fields': ('username', 'password')}),  
        ('Información personal', {'fields': ('nombre', 'apellido', 'email', 'telefono', 'CUIG', 'id_rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Campos visibles al crear un usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'CUIT', 'nombre', 'apellido', 'email', 'telefono', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'CUIT','email', 'nombre', 'apellido')
    ordering = ('username', 'CUIT')
    
    
# @admin.register(SolicitudEstablecimiento)
# class SolicitudEstablecimientoAdmin(admin.ModelAdmin):
#     list_display = ("nombre", "CUIG", "usuario", "estado", "fecha_solicitud")
#     list_filter = ("estado",)
#     actions = ["aprobar_solicitudes"]

#     def aprobar_solicitudes(self, request, queryset):
#         aprobadas = 0
#         for solicitud in queryset:
#             if solicitud.estado == "pendiente":
#                 solicitud.aprobar()
#                 aprobadas += 1
#         self.message_user(request, f"{aprobadas} solicitudes aprobadas correctamente.")

#     aprobar_solicitudes.short_description = "Aprobar solicitudes seleccionadas"
    
    

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol)
admin.site.register(Establecimiento)
admin.site.register(Cuidador)
# admin.site.register(SolicitudEstablecimiento, SolicitudEstablecimientoAdmin)