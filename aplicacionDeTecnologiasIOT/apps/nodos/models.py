from django.db import models

<<<<<<< HEAD
# Create your models here.
=======
class Nodo(models.Model):
    id_nodo = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField()
    lat = models.CharField()
    lon = models.CharField()
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.id_nodo} - {self.fecha_hora}'
>>>>>>> 4ce9c4b797368c6f7ad97fd4325cae40ee8b0453
