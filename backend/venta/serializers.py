from rest_framework import serializers
from .models import Venta

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ('id', 'marca', 'modelo', 'precio', 'anio')
        read_only_fields = ('id',)

#comenta para que sirve este codigo y que hace
#Este código define un serializador para la entidad Venta.
#Se define la clase VentaSerializer que hereda de serializers.ModelSerializer.
#Se define la clase Meta que contiene la información del modelo y los campos que se van a serializar.
#Se define el modelo como Venta y los campos que se van a serializar como id, marca, modelo, precio y anio.
#Se define el campo id como de solo lectura para que no se pueda modificar al crear o actualizar una venta.
