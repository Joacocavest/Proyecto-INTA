from django.contrib import admin
from .models import Nodo, Lectura

@admin.register(Nodo)
class NodoAdmin(admin.ModelAdmin):
    list_display = ('id_nodo', 'modelo_gps', 'bateria', 'activo', 'defectuoso', 'codigo')
    list_filter = ('activo', 'defectuoso', 'modelo_gps')
    search_fields = ('id_nodo', 'codigo')
    fields = ('id_nodo', 'modelo_gps', 'bateria', 'activo', 'defectuoso', 'codigo')
    
    # Colores para los estados
    def get_list_display_links(self, request, list_display):
        return ['id_nodo']
    
    # Personalizar el display de activo/defectuoso
    def activo(self, obj):
        return "✅ Activo" if obj.activo else "❌ Inactivo"
    activo.short_description = "Estado"
    
    def defectuoso(self, obj):
        return "⚠️ Defectuoso" if obj.defectuoso else "✅ Funcionando"
    defectuoso.short_description = "Condición"

@admin.register(Lectura)
class LecturaAdmin(admin.ModelAdmin):
    list_display = ('id_nodo', 'fecha_hora', 'latitud', 'longitud', 'contador')
    list_filter = ('fecha_hora', 'id_nodo', 'contador')
    search_fields = ('id_nodo__id_nodo', 'latitud', 'longitud')
    date_hierarchy = 'fecha_hora'
    fields = ('id_nodo', 'fecha_hora', 'latitud', 'longitud', 'contador')
    raw_id_fields = ('id_nodo',)  # Para facilitar búsqueda de nodos
    
    # Mostrar lecturas más recientes primero
    ordering = ['-fecha_hora']