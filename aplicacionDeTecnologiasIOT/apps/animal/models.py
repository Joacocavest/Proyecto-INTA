from django.db import models

# MODELO ANIMAL
class Animal(models.Model):
    carabana = models.CharField(primary_key=True, blank=False, null=False, unique=True)
    CUIG = models.ForeignKey("usuario.Establecimiento", on_delete=models.CASCADE, related_name='animal_establecimiento')
    id_especie = models.ForeignKey("animal.Especie", on_delete=models.CASCADE, related_name='animal_especie')
    id_raza = models.ForeignKey("animal.Raza", on_delete=models.CASCADE, related_name='animal_raza')
    id_nodo = models.OneToOneField("nodos.Nodo", on_delete=models.CASCADE, related_name='animal_nodo', blank=True, null=True)
    id_cuidador = models.ForeignKey("usuario.Cuidador", on_delete=models.CASCADE, related_name='animal_cuidador')
    
    def __str__(self):
        return f'{self.carabana} - {self.id_especie.nombre_especie} ({self.id_raza.nombre_raza})'

    

# MODELO ESPECIE
class Especie(models.Model):
    nombre_especie = models.CharField(max_length=50, unique=True, blank=False, null=False)
    id_raza = models.ForeignKey("animal.Raza", on_delete=models.CASCADE, related_name='especie_raza')
    
    def __str__(self):
        return f'{self.id}, {self.nombre_especie}'
    
# MODELO RAZA
class Raza(models.Model):
    nombre_raza = models.CharField(max_length=50, unique=True, blank=False, null=False)
    
    def __str__(self):
        return f'{self.id}, {self.nombre_raza}'
