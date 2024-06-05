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

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    direccion = models.CharField(max_length=50)


class Boleta(models.Model):
    id = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    total = models.IntegerField()


class despacho(models.Model):
    id = models.AutoField(primary_key=True)
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    direccion = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)



