from django.shortcuts import get_object_or_404, render
from apps.animal.models import Animal, Especie, Raza


#VISTA PARA LISTAR LOS ANIMALES#
def lista_animales(request):
    animales = Animal.objects.all()
    return render(request, 'animal/lista_animales.html', {'animales':animales})

#VISTA PARA VER UN ANIMAL:
def animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'animal/animal.html', {'animal':animal})




#VISTA PARA LISTAR LAS ESPECIES#
def lista_especies(request):
    especies = Especie.objects.all()
    return render(request, 'especie/lista_especies.html', {'especies':especies})

#VISTA PARA VER UNA ESPECIE:
def especie(request, pk):
    especie = get_object_or_404(Especie, pk=pk)
    return render(request, 'especie/especie.html', {'especie':especie})




#VISTA PARA LISTAR LAS RAZAS#
def lista_razas(request):
    razas = Raza.objects.all()
    return render(request, 'raza/lista_razas.html', {'razas':razas})

#VISTA PARA VER UNA RAZA 
def raza(request, pk):
    raza = get_object_or_404(Raza, pk=pk)
    return render(request, 'raza/raza.html', {'raza':raza})