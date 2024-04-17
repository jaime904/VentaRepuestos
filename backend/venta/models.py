from django.db import models

# Create your models here.
class Venta(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    precio = models.IntegerField()
    anio = models.IntegerField()