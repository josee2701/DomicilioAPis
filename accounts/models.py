# Create your models here.
# accounts/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    # Sobrescribimos groups para que tenga un related_name distinto
    groups = models.ManyToManyField(
        Group,
        verbose_name="grupos",
        blank=True,
        help_text="Los grupos a los que pertenece este usuario.",
        related_name="customuser_set",        
        related_query_name="customuser",      
    )
    # Sobrescribimos user_permissions para que no choque
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="permisos de usuario",
        blank=True,
        help_text="Permisos específicos para este usuario.",
        related_name="customuser_permissions",   
        related_query_name="customuser_permission",
    )
    pass

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="client_profile")


class Driver(models.Model):
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('busy',      'Ocupado'),
        ('inactive',  'Inactivo'),
    ]
    user     = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="driver_profile")
    status   = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
