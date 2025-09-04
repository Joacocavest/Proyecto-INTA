from django.contrib import admin
from .models import Animal, Especie, Raza

@admin.register(Raza)
class RazaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_raza')
    search_fields = ('nombre_raza',)
    fields = ('nombre_raza',)

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_especie', 'id_raza')
    list_filter = ('id_raza',)
    search_fields = ('nombre_especie',)
    fields = ('nombre_especie', 'id_raza')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('carabana', 'get_especie', 'get_raza', 'id_nodo', 'CUIG', 'get_cuidador')
    list_filter = ('id_especie', 'id_raza', 'CUIG')
    search_fields = ('carabana', 'id_nodo__id_nodo', 'CUIG__nombre')
    fields = ('carabana', 'CUIG', 'id_especie', 'id_raza', 'id_nodo', 'id_cuidador')
    raw_id_fields = ('id_nodo', 'id_cuidador')  # Para facilitar selección
    
    # Métodos para mostrar información más clara
    def get_especie(self, obj):
        return obj.id_especie.nombre_especie
    get_especie.short_description = 'Especie'
    
    def get_raza(self, obj):
        return obj.id_raza.nombre_raza
    get_raza.short_description = 'Raza'
    
    def get_cuidador(self, obj):
        return f"{obj.id_cuidador.nombre_cuidador} {obj.id_cuidador.apellido_cuidador}"
    get_cuidador.short_description = 'Cuidador'