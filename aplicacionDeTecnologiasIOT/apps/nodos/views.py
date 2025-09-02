from django.shortcuts import get_object_or_404, render, redirect
from apps.nodos.models import Nodo, Lectura
from .forms import NodoForm

#VISTA PARA CREAR UN NODO#
def crear_nodo(request):
    if request.method == "POST":
        form = NodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nodos:lista_nodos')  # redirige a la lista de nodos
    else:
        form = NodoForm()
    return render(request, 'nodos/agregar_nodo.html', {'form': form})

#VISTA PARA MODIFICAR UN NODO#
def modificar_nodo(request, pk):
    nodo = get_object_or_404(Nodo, pk=pk)
    if request.method == "POST":
        form = NodoForm(request.POST, instance=nodo)
        if form.is_valid():
            form.save()
            return redirect('nodos:lista_nodos')
    else:
        form = NodoForm(instance=nodo)
    return render(request, 'nodos/modificar_nodo.html', {'form': form})

#VISTA PARA ELIMINAR UN NODO#
def eliminar_nodo(request, pk):
    nodo = get_object_or_404(Nodo, pk=pk)
    if request.method == "POST":
        nodo.delete()
        return redirect('nodos:lista_nodos')
    return render(request, 'nodos/eliminar_nodo.html', {'nodo': nodo})

#VISTA PARA LISTAR LOS NODOS#
def lista_nodos(request):
    nodos = Nodo.objects.all()
    # Lógica de búsqueda
    query = request.GET.get('q')
    if query:
        nodos = nodos.filter(id_nodo__icontains=query)
    return render(request, 'nodos/lista_nodos.html', {'nodos':nodos})

#VISTA PARA VER UN NODO
def nodo(request, pk):
    nodo = get_object_or_404(Nodo, pk=pk)
    return render(request, 'nodo/nodo.html', {'nodo':nodo})



#VISTA PARA LISTAR LAS LECTURAS#
def lista_lecturas(request):
    lecturas = Lectura.objects.all()
    return render(request, 'lectura/lista_lecturas.html', {'lecturas':lecturas})

#VISTA PARA VER UNA LECTURA
def lectura(request, pk):
    lectura = get_object_or_404(Lectura, pk=pk)
    return render(request, 'lectura/lectura.html', {'lectura':lectura})
