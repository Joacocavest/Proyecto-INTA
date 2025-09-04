# forms.py
from django import forms
from .models import Nodo
from apps.animal.models import Animal
from django.db.models import Q


class NodoForm(forms.ModelForm):
    animal = forms.ModelChoiceField(
            queryset=Animal.objects.filter(id_nodo__isnull=True),  # solo animales libres
            required=False,
            label="Asignar a Animal"
        )
    class Meta:
        model = Nodo
        fields = ['id_nodo', 'activo', 'defectuoso', 'modelo_gps', 'bateria', 'codigo']
        widgets = {
            'id_nodo': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo_gps': forms.TextInput(attrs={'class': 'form-control'}),
            'bateria': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'codigo': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        nodo = kwargs.get("instance")
        super().__init__(*args, **kwargs)
        # Si es edición (tiene instancia con PK), deshabilitamos id_nodo
        if nodo:  
            # Si es modificación, incluir también el animal actual
            self.fields["animal"].queryset = Animal.objects.filter(
                Q(id_nodo__isnull=True) | Q(id_nodo=nodo)
            )
            try:
                self.fields["animal"].initial = nodo.animal_nodo.first()
            except:
                self.fields["animal"].initial = None