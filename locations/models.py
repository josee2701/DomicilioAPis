from django.db import models

from accounts.models import Client


class Address(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=50)  
    street = models.CharField(max_length=200)
    apartment   = models.CharField(
        max_length=50,
        blank=True, null=True,
        help_text="Piso, apto, unidad, etc."
    )
    city = models.CharField(max_length=100)
    country     = models.CharField(
        max_length=100,
        default='Colombia'
    )
    # aquí guardamos ambos: lat y lon
    # point       = gis_models.PointField(
    #     geography=True,  # cálculos en metros/kms sin reproyección
    #     srid=4326
    # )
    