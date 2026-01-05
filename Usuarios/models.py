from django.db import models
from django.contrib.auth.models import AbstractUser
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    url_imagen = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    class Rol(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        STAFF = 'staff', 'Staff'
        ADMIN = 'admin', 'Admin'
    rol = models.CharField(max_length=10, choices=Rol.choices, default=Rol.CLIENTE)

    def __str__(self):
        return self.first_name + " " + self.last_name
