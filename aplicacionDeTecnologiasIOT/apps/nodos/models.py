from django.db import models
from django.utils import timezone

# MODELO NODO
class Nodo(models.Model):
    id_nodo = models.CharField(primary_key=True, max_length=15, unique=True, null=False, blank=False)
    activo = models.BooleanField(default=True, blank=False, null=False) #cuando activo = True, significa que está activo el nodo.
    defectuoso = models.BooleanField(default=False, blank=False, null=False) #cuando defectuoso = True, significa que esta defectuoso el nodo.
    modelo_gps = models.CharField(max_length=100, blank=True, null=True)
    bateria = models.IntegerField(default=100, blank=False, null=False)
    codigo = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.id_nodo}, Activo: {self.activo}, Defectuoso: {self.defectuoso}, Batería: {self.bateria}'

    
    
    
# MODELO LECTURA
class Lectura(models.Model):
    id_nodo = models.ForeignKey("nodos.Nodo", on_delete=models.CASCADE, related_name='lectura_nodo')
    fecha_hora = models.DateTimeField(primary_key=True, blank=False, null=False, default=timezone.now)
    latitud = models.CharField(blank=False, null=False, max_length=30)
    longitud = models.CharField(blank=False, null=False, max_length=30)
    contador = models.IntegerField(default=0, blank=True, null=True) #cuando contador llegue a 6 lecturas repetidas, en el modelo Nodo, defectuoso=True
    
    def __str__(self):
        return f'{self.id_nodo}, {self.fecha_hora}'
    
    def save(self, *args, **kwargs):
        ultima_lectura = Lectura.objects.filter(id_nodo=self.id_nodo).order_by("-id").first()
        if ultima_lectura and ultima_lectura.fecha_hora == self.fecha_hora:
            self.contador = self.contador + 1
        super().save(*args, **kwargs)