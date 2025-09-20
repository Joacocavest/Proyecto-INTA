from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = '__all__'

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        
class UsuarioRegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            "nombre",
            "apellido",
            "CUIT",
            "nombre_usuario",
            "email",
            "telefono",
            "id_rol",
            "password1",
            "password2",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "CUIT": forms.NumberInput(attrs={"class": "form-control"}),
            "nombre_usuario": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "id_rol": forms.Select(attrs={"class": "form-control"}),
        }
