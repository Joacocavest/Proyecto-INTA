from django.db import models
from django.contrib.auth.models import AbstractUser


# MODELO USUARIO
class Usuario(AbstractUser):
    CUIG = models.ForeignKey("usuario.Establecimiento", on_delete=models.CASCADE, related_name='usuario_establecimiento'),
    CUIT = models.BigIntegerField(primary_key=True, unique=True, null=False, blank=True)
    nombre = models.CharField(max_length=2, blank=False)
    apellido = models.CharField(max_length=3, blank=False)
    nombre_usuario = models.CharField(max_length=3, blank=False, unique=True)
    contraseña = models.CharField(max_length=3, blank=False, unique=True)
    email = models.EmailField(unique=True, blank=False)
    telefono = models.CharField(max_length=10, blank=True)
    id_rol = models.ForeignKey("usuario.Rol", on_delete=models.CASCADE, related_name='rol')

    def __str__(self):
        return f'{self.nombre}, {self.apellido}, {self.nombre_usuario}, {self.CUIG} {self.email}'




# MODELO CUIDADOR
class Cuidador(models.Model):
    CUIT = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)
    CUIG = models.ForeignKey("usuario.Establecimiento", on_delete=models.CASCADE, related_name='cuidador_establecimiento')
    sector = models.CharField(max_length=15, blank=True, null=True)
    nombre_cuidador = models.CharField(max_length=2, blank=False)
    apellido_cuidador = models.CharField(max_length=3, blank=False)
    email = models.EmailField(unique=True, blank=False)
    telefono = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.nombre_cuidador}, {self.apellido_cuidador}, {self.CUIT}, {self.CUIG}"




# MODELO ROL
class Rol(models.Model):
    nombre_rol = models.CharField(max_length=15, unique=True, null=False, blank=False)
    descripcion_rol = models.CharField(max_length=1500, unique=True, null=False, blank=False)




#MODELO ESTABLECIMIENTO    
class Establecimiento(models.Model):
    CUIG = models.CharField(max_length=8, primary_key=True, unique=True)
    provincia = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="establecimientos/logos/", blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.CUIG})"
    
    
    

