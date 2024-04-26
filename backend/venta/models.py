from django.db import models

# Create your models here.
class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    modelo = models.CharField(max_length=50)
    precio = models.IntegerField()
    anio = models.IntegerField()