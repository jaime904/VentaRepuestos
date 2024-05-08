from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    modelo = models.CharField(max_length=50)
    precio = models.IntegerField()
    anio = models.IntegerField()

class Boleta(models.Model):
    id = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    total = models.IntegerField()
