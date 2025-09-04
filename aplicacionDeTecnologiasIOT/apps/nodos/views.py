from django.shortcuts import get_object_or_404, render, redirect
from apps.nodos.models import Nodo, Lectura
from .forms import NodoForm
from django.db.models import Prefetch
from apps.animal.models import Animal, Especie, Raza


#VISTA PARA AGREGAR + MODIFICAR NODO#
def nodo_form(request, pk=None):
    nodo = get_object_or_404(Nodo, pk=pk) if pk else None

    if request.method == "POST":
        form = NodoForm(request.POST, instance=nodo)
        if form.is_valid():
            nodo = form.save()
            animal = form.cleaned_data.get("animal")
            if animal:
                animal.id_nodo = nodo
                animal.save()
                return redirect("nodos:lista_nodos")
    else:
        form = NodoForm(instance=nodo)

    return render(request, "nodos/nodo_form.html", {"form": form, "nodo": nodo})


#VISTA PARA ELIMINAR UN NODO#
def eliminar_nodo(request, pk):
    nodo = get_object_or_404(Nodo, pk=pk)
    if request.method == "POST":
        nodo.delete()
        return redirect('nodos:lista_nodos')
    return render(request, 'nodos/eliminar_nodo.html', {'nodo': nodo})

#VISTA PARA LISTAR LOS NODOS + BUSCAR#
def lista_nodos(request):
    # Base queryset con prefetch de animales, especie y raza
    nodos = Nodo.objects.all().prefetch_related(
        Prefetch("animal_nodo", queryset=Animal.objects.select_related("id_especie", "id_raza"))
    )

    # filtros desde GET
    query = request.GET.get("q")
    especie = request.GET.get("especie")
    raza = request.GET.get("raza")

    if query:
        nodos = nodos.filter(id_nodo__icontains=query)

    if especie:
        nodos = nodos.filter(animal_nodo__id_especie__nombre_especie=especie)

    if raza:
        nodos = nodos.filter(animal_nodo__id_raza__nombre_raza=raza)

    # para armar dinámicamente los <select>
    especies = Especie.objects.all()
    razas = Raza.objects.all()

    return render(
        request,
        "nodos/lista_nodos.html",
        {
            "nodos": nodos,
            "especies": especies,
            "razas": razas,
        },
    )

#VISTA PARA VER UN NODO
def nodo(request, pk):
    nodo = get_object_or_404(Nodo, pk=pk)
    return render(request, 'nodo/nodo.html', {'nodo':nodo})



#VISTA PARA LISTAR LAS LECTURAS#
def lista_lecturas(request, nodo_id=None):
    if nodo_id:
        lecturas = Lectura.objects.filter(id_nodo=nodo_id)
    else:
        lecturas = Lectura.objects.all()
    return render(request, 'lectura/lista_lecturas.html', {'lecturas': lecturas})

#VISTA PARA VER UNA LECTURA
def lectura(request, pk):
    lectura = get_object_or_404(Lectura, pk=pk)
    return render(request, 'lectura/lectura.html', {'lectura':lectura})
