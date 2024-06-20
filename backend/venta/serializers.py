from rest_framework import serializers
from .models import Carrito, CarritoVenta, Venta, Boleta, Cliente , despacho

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ('id', 'marca', 'modelo', 'precio', 'anio', 'estado')

class BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleta
        fields = ['id', 'venta', 'cliente', 'fecha', 'cantidad', 'total']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'rut', 'nombre', 'apellido', 'telefono', 'email', 'direccion')

class DespachoSerializer(serializers.ModelSerializer):  
    class Meta:
        model = despacho
        fields = ('id', 'boleta', 'fecha', 'direccion', 'estado')


    