from rest_framework import serializers
from .models import Carrito, CarritoVenta, Venta, Boleta, Cliente, despacho  # Asegúrate de que 'despacho' está en minúsculas

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ('id', 'marca', 'modelo', 'precio', 'anio', 'estado')

class BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleta
        fields = ['id', 'venta', 'cliente', 'fecha', 'cantidad', 'total']
        extra_kwargs = {
            'venta': {'required': False}  # Hacer que el campo 'venta' no sea obligatorio
        }

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'rut', 'nombre', 'apellido', 'telefono', 'email', 'direccion')

class DespachoSerializer(serializers.ModelSerializer):  
    class Meta:
        model = despacho
        fields = ('id', 'boleta', 'fecha', 'direccion', 'estado')

class CarritoVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarritoVenta
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    ventas = CarritoVentaSerializer(many=True, read_only=True, source='carritoventa_set')
    
    class Meta:
        model = Carrito
        fields = '__all__'
