from django.db import models

class Nodo(models.Model):
    id_nodo = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField()
    lat = models.CharField()
    lon = models.CharField()

    def __str__(self):
        return f'{self.id_nodo} - {self.fecha_hora}'