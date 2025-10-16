# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import Usuario

# class UsuarioCreationForm(UserCreationForm):
#     class Meta:
#         model = Usuario
#         fields = '__all__'

# class UsuarioChangeForm(UserChangeForm):
#     class Meta:
#         model = Usuario
#         fields = '__all__'
        
# class UsuarioRegistroForm(UserCreationForm):
#     class Meta:
#         model = Usuario
#         fields = [
#             "nombre",
#             "apellido",
#             "CUIT",
#             "email",
#             "telefono",
#             "id_rol",
            
#             "username",
#             "password1",
#             "password2",
            
#             "CUIG"
#         ]




from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

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
            "id_rol",
            "username",
            "password1",
            "password2",
            "CUIG",
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Rol
        self.fields['id_rol'].queryset = Rol.objects.filter(nombre_rol__in=["Administrador", "Usuario"])

    def clean_CUIT(self):
        cuit = self.cleaned_data.get('CUIT')
        if not cuit:
            raise forms.ValidationError("El CUIT es obligatorio.")
        s = str(cuit)
        if len(s) != 11:
            raise forms.ValidationError("El CUIT debe tener 11 dígitos.")
        return cuit