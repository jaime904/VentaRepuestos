from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .models import Cliente, Venta, Boleta , despacho
from .serializers import ClienteSerializer, DespachoSerializer, VentaSerializer, BoletaSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    permission_classes = [AllowAny]
    serializer_class = VentaSerializer

    @action(detail=False, methods=['post']) # sirve para crear una venta
    def create_venta(self, request):
        data_nueva = request.data
        data_nueva['estado'] = True
        serializer = VentaSerializer(data=data_nueva)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get']) # sirve para obtener todas las ventas
    def devolverListado(self, request):
        query = Venta.objects.all()
        serializer = VentaSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST']) # sirve para crear una venta con boletas
    def create_venta_con_boletas(self, request):
        venta_id = request.data.get('venta')        
        venta = get_object_or_404(Venta, pk=venta_id)
        boletas_data = request.data
        boletas_data['venta_id'] = venta
        boletas_serializer = BoletaSerializer(data=boletas_data)
        if boletas_serializer.is_valid():
            boletas_serializer.save()  
            boletas_data = boletas_serializer.data  
            precio_venta = venta.precio
            anio_venta = venta.anio
            return Response({
                'precio_venta': precio_venta,
                'anio_venta': anio_venta,
                'boletas': boletas_data
            }, status=status.HTTP_201_CREATED)
        return Response(boletas_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get']) # sirve para obtener las boletas con venta
    def obtener_boletas_con_venta(self, request):
        boletas = Boleta.objects.select_related('venta', 'cliente').all()
        data = []
        for boleta in boletas:
            data.append({
                'id_boleta': boleta.id,
                'fecha': boleta.fecha,
                'cantidad': boleta.cantidad,
                'total': boleta.total,
                'venta': {
                    'id_venta': boleta.venta.id,
                    'marca': boleta.venta.marca,
                    'modelo': boleta.venta.modelo,
                    'estado': boleta.venta.estado,
                    'precio': boleta.venta.precio,
                    'anio': boleta.venta.anio,
                },
                'cliente': {
                    'id_cliente': boleta.cliente.id if boleta.cliente else None,
                    'rut': boleta.cliente.rut if boleta.cliente else None,
                    'nombre': boleta.cliente.nombre if boleta.cliente else None,
                    'apellido': boleta.cliente.apellido if boleta.cliente else None,
                    'telefono': boleta.cliente.telefono if boleta.cliente else None,
                    'email': boleta.cliente.email if boleta.cliente else None,
                    'direccion': boleta.cliente.direccion if boleta.cliente else None
                }
            })
        return JsonResponse(data, safe=False)

    @action(detail=True, methods=['put', 'patch'])
    def actualizar_venta(self, request, pk=None): # sirve para modificar una venta
        venta = self.get_object()
        serializer = VentaSerializer(venta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post']) # sirve para crear un Cliente
    def create_cliente(self, request):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get']) # sirve para obtener todos los clientes
    def devolverListadoClientes(self, request):
        query = Cliente.objects.all()
        serializer = ClienteSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])  # Sirve para crear un despacho
    def create_despacho(self, request):
        data = request.data
        boleta_id = data.get('boleta')
        boleta = get_object_or_404(Boleta, pk=boleta_id)
        data['boleta'] = boleta.id  # Asegúrate de enviar el ID de la boleta en la solicitud
        serializer = DespachoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])  # Sirve para obtener los despachos con el ID de la boleta asociada
    def obtener_despachos_con_boletas(self, request):
        despachos = despacho.objects.select_related('boleta').all()
        serializer = DespachoSerializer(despachos, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs): # sirve para modificar el estado de la venta y cambiarlo a falso 
        try:
            instance = self.get_object()
            instance.estado = False  # Cambia el estado a falso
            instance.save()          # Guarda el cambio en la base de datos
            return JsonResponse({"message": "Estado de venta cambiado a falso"})
        except Venta.DoesNotExist:
            return JsonResponse({"error": "La venta no existe"})
