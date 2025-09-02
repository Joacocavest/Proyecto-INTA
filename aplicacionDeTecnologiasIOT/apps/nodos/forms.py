# forms.py
from django import forms
from .models import Nodo

class NodoForm(forms.ModelForm):
    class Meta:
        model = Nodo
        fields = ['id_nodo', 'activo', 'defectuoso', 'modelo_gps', 'bateria', 'codigo']
        widgets = {
            'id_nodo': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo_gps': forms.TextInput(attrs={'class': 'form-control'}),
            'bateria': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'codigo': forms.NumberInput(attrs={'class': 'form-control'}),
        }
