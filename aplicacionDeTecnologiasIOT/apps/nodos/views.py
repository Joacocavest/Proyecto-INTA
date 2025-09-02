from django.shortcuts import get_object_or_404, render
from apps.nodos.models import Nodo, Lectura


#VISTA PARA LISTAR LOS NODOS#
def lista_nodos(request):
    nodos = Nodo.objects.all()
    return render(request, 'nodo/lista_nodos.html', {'nodos':nodos})

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
