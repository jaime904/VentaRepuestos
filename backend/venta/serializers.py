from rest_framework import serializers
from .models import Venta, Boleta

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ('id', 'marca', 'modelo', 'precio', 'anio', 'estado')

class BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleta
        fields = ('id', 'venta', 'fecha', 'cantidad', 'total')