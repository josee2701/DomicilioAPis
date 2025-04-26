from django.db import models

from accounts.models import Client, Driver
from locations.models import Address


# Create your models here.
class Service(models.Model):
    STATUS_CHOICES = [
        ('requested','Requested'),
        ('assigned','Assigned'),
        ('in_transit','In Transit'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
    ]
    client= models.ForeignKey(Client, on_delete=models.CASCADE, related_name='services')
    driver= models.ForeignKey(Driver, null=True, blank=True,on_delete=models.SET_NULL, related_name='services')
    pickup_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='+')
    eta_minutes = models.IntegerField(null=True, blank=True, help_text="Estimación de llegada en minutos")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    date_aplication = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)