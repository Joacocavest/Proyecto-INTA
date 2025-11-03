from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone


# MODELO USUARIO
class Usuario(AbstractUser):
    CUIG = models.ForeignKey("usuario.Establecimiento", on_delete=models.CASCADE, null=True, blank=True, related_name='usuarios')
    CUIT = models.BigIntegerField(unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    id_rol = models.ForeignKey("usuario.Rol", on_delete=models.SET_NULL, related_name='usuario', null=True, blank=True)

    
    USERNAME_FIELD = 'username'  #o 'email' si queremos usar email como login
    REQUIRED_FIELDS = ['email', 'CUIT', 'nombre', 'apellido']

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.username}) - {self.CUIG if self.CUIG else "Sin Establecimiento"}'




# MODELO CUIDADOR
class Cuidador(models.Model):
    CUIT = models.BigIntegerField(primary_key=True, unique=True, null=False, blank=False)
    CUIG = models.ForeignKey("usuario.Establecimiento", on_delete=models.CASCADE, related_name='cuidador_establecimiento')
    sector = models.CharField(max_length=15, blank=True, null=True)
    nombre_cuidador = models.CharField(max_length=2, blank=False)
    apellido_cuidador = models.CharField(max_length=3, blank=False)
    email = models.EmailField(unique=True, blank=False)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nombre_cuidador}, {self.apellido_cuidador}, {self.CUIT}, {self.CUIG}"




# MODELO ROL
class Rol(models.Model):
    nombre_rol = models.CharField(max_length=30, unique=True, null=False, blank=False)
    descripcion_rol = models.CharField(max_length=1500, null=False, blank=False)
    
    def __str__(self):
        return self.nombre_rol




#MODELO ESTABLECIMIENTO    
class Establecimiento(models.Model):
    CUIG = models.CharField(max_length=15, primary_key=True, unique=True)
    provincia = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="establecimientos/logos/", blank=True, null=True)
    
    #campo opcional: quién creó este establecimiento
    creado_por = models.ForeignKey("usuario.Usuario", on_delete=models.SET_NULL, null=True, blank=True, related_name="establecimientos_creados"
    )

    def __str__(self):
        return f"{self.nombre} ({self.CUIG})"
    
# #MODELO PARA ENVIAR UNA SOLICITUD DE ACEPTACIÓN DEL ESTABLECIMIENTO
# class SolicitudEstablecimiento(models.Model):
#     usuario = models.ForeignKey("usuario.Usuario", on_delete=models.CASCADE)
#     nombre_establecimiento = models.CharField(max_length=100)
#     CUIG = models.CharField(max_length=20, unique=True)
#     provincia = models.CharField(max_length=50)
#     departamento = models.CharField(max_length=50)
#     localidad = models.CharField(max_length=50)
#     direccion = models.CharField(max_length=100)
#     fecha_solicitud = models.DateTimeField(auto_now_add=True)
#     estado = models.CharField(
#         max_length=20,
#         choices=[("Pendiente", "Pendiente"), ("Aprobada", "Aprobada"), ("Rechazada", "Rechazada")],
#         default="Pendiente")

#     def __str__(self):
#         return f"{self.nombre_establecimiento} ({self.CUIG}) ({self.estado})"
    
    
#     def aprobar(self):
#         """Crea el establecimiento y activa al usuario como administrador."""
#         from usuario.models import Rol, Establecimiento  # Import aquí para evitar dependencias circulares

#         # 1 Crear establecimiento real
#         establecimiento, created = Establecimiento.objects.get_or_create(
#             CUIG=self.CUIG,
#             defaults={
#                 "nombre": self.nombre_establecimiento,
#                 "provincia": self.provincia,
#                 "departamento": self.departamento,
#                 "localidad": self.localidad,
#                 "direccion": self.direccion,
#             },
#         )

#         # 2 Activar usuario y asignar rol administrador
#         rol_admin = Rol.objects.get_or_create(nombre="Administrador")[0]
#         usuario = self.usuario
#         usuario.is_active = True
#         usuario.id_rol = rol_admin
#         usuario.CUIG = establecimiento
#         usuario.estado = "activo"
#         usuario.save()

#         # 3 Cambiar estado de la solicitud
#         self.estado = "aprobada"
#         self.save()

#         return establecimiento
    
# # MODELO PARA INVITAR A USUARIOS
# class InvitacionUsuario(models.Model):
#     ESTADOS_INVITACION = [
#         ('pendiente', 'Pendiente'),
#         ('aceptada', 'Aceptada'),
#         ('rechazada', 'Rechazada'),
#         ('expirada', 'Expirada'),
#     ]

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     email = models.EmailField()
#     rol = models.ForeignKey("usuario.Rol", on_delete=models.SET_NULL, null=True, blank=True)
#     establecimiento = models.ForeignKey("usuario.Establecimiento", on_delete=models.CASCADE)
#     invitado_por = models.ForeignKey("usuario.Usuario", on_delete=models.CASCADE, related_name="invitaciones_enviadas")
#     token = models.CharField(max_length=100, unique=True)
#     estado = models.CharField(max_length=20, choices=ESTADOS_INVITACION, default="pendiente")
#     fecha_envio = models.DateTimeField(auto_now_add=True)
#     fecha_aceptacion = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"Invitación a {self.email} ({self.estado})"

#     def aceptar(self, usuario):
#         """Asocia la invitación a un usuario existente y lo activa."""
#         usuario.CUIG = self.establecimiento
#         usuario.id_rol = self.rol
#         usuario.is_active = True
#         usuario.save()

#         self.estado = "aceptada"
#         self.fecha_aceptacion = timezone.now()
#         self.save()



