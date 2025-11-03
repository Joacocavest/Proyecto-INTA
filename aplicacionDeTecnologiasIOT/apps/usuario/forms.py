


from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario, Rol
import uuid


class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            "username",
            "nombre",
            "apellido",
            "CUIT",
            "email",
            "telefono",
            "id_rol",
            "CUIG",
            "password1",
            "password2",
        ]

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = [
            "username",
            "nombre",
            "apellido",
            "CUIT",
            "email",
            "telefono",
            "id_rol",
            "CUIG",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

class UsuarioRegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            "nombre",
            "apellido",
            "CUIT",
            "email",
            "telefono",
            "username",
            "password1",
            "password2",
        ]
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     from .models import Rol
    #     self.fields['id_rol'].queryset = Rol.objects.filter(nombre_rol__in=["Administrador", "Empleado"])

    def clean_CUIT(self):
        cuit = self.cleaned_data.get('CUIT')
        if not cuit:
            raise forms.ValidationError("El CUIT es obligatorio.")
        s = str(cuit)
        if len(s) != 11:
            raise forms.ValidationError("El CUIT debe tener 11 dígitos.")
        return cuit
    
    
    
    
# class SolicitudEstablecimientoForm(forms.ModelForm):
#     class Meta:
#         model = SolicitudEstablecimiento
#         fields = ["nombre_establecimiento", "CUIG", "provincia", "departamento", "localidad", "direccion"]
        
        
        

# class InvitacionUsuarioForm(forms.ModelForm):
#     class Meta:
#         model = InvitacionUsuario
#         fields = ['email', 'rol']

#     def __init__(self, *args, **kwargs):
#         establecimiento = kwargs.pop('establecimiento', None)
#         invitado_por = kwargs.pop('invitado_por', None)
#         super().__init__(*args, **kwargs)
#         self.establecimiento = establecimiento
#         self.invitado_por = invitado_por

#     def save(self, commit=True):
#         invitacion = super().save(commit=False)
#         invitacion.establecimiento = self.establecimiento
#         invitacion.invitado_por = self.invitado_por
#         invitacion.token = uuid.uuid4().hex
#         if commit:
#             invitacion.save()
#         return invitacion

        