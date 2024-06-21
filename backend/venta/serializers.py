from rest_framework import serializers
from .models import BoletaVenta, Carrito, CarritoVenta, Venta, Boleta, Cliente, despacho  # Asegúrate de que 'despacho' está en minúsculas

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ('id', 'marca', 'modelo', 'precio', 'anio', 'estado')

class BoletaSerializer(serializers.ModelSerializer):
    ventas = serializers.SerializerMethodField()

    class Meta:
        model = Boleta
        fields = ['id', 'cliente', 'fecha', 'cantidad', 'total', 'ventas']

    def get_ventas(self, obj):
        boleta_ventas = BoletaVenta.objects.filter(boleta=obj)
        return BoletaVentaSerializer(boleta_ventas, many=True).data

    def create(self, validated_data):
        # Crear la boleta
        boleta = Boleta.objects.create(**validated_data)
        
        # Obtener ventas del carrito desde el contexto
        ventas_en_carrito = self.context.get('ventas_en_carrito')
        
        # Crear las relaciones Boleta-Venta
        for item in ventas_en_carrito:
            BoletaVenta.objects.create(boleta=boleta, venta=item.venta)
        
        return boleta

class BoletaVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoletaVenta
        fields = ['boleta', 'venta']



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
