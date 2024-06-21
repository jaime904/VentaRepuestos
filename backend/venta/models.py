from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    modelo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    precio = models.IntegerField()
    anio = models.IntegerField()


class Vendedor(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    direccion = models.CharField(max_length=50)


class Boleta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    venta = models.ForeignKey(Venta, null=True, blank=True, on_delete=models.SET_NULL)  # Permitir valores nulos para venta


class BoletaVenta(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)


class nota_credito(models.Model):   
    id = models.AutoField(primary_key=True)
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    total = models.IntegerField()
    cantidad = models.IntegerField()
    estado = models.BooleanField(default=True)


class despacho(models.Model):
    id = models.AutoField(primary_key=True)
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    direccion = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)


class Carrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class CarritoVenta(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)