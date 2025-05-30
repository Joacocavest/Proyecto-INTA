from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    apellido_nombre = models.CharField(max_length=25, blank=False)
    email = models.EmailField(unique=True, blank=False)
    telefono = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f'{self.apellido_nombre}; {self.email}'
    
     
    
