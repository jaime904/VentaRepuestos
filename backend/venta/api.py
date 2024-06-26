from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .models import BoletaVenta, Carrito, CarritoVenta, Cliente, Venta, Boleta , despacho
from .serializers import ClienteSerializer, DespachoSerializer, VentaSerializer, BoletaSerializer , CarritoVentaSerializer, CarritoSerializer , BoletaVentaSerializer
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



    @action(detail=False, methods=['post'])
    def create_venta_con_boletas(self, request):
        cliente_id = request.data.get('cliente_id')
        print(f'Cliente ID recibido: {cliente_id}')
        cliente = get_object_or_404(Cliente, pk=cliente_id)

        # Verificar si el cliente tiene un carrito
        carrito = get_object_or_404(Carrito, cliente=cliente)
        ventas_en_carrito = CarritoVenta.objects.filter(carrito=carrito)

        if not ventas_en_carrito.exists():
            return Response({'error': 'El carrito está vacío'}, status=status.HTTP_400_BAD_REQUEST)

        # Calcular el total de todas las ventas en el carrito
        total = sum(item.cantidad * item.venta.precio for item in ventas_en_carrito)
        cantidad_total = sum(item.cantidad for item in ventas_en_carrito)
        
        # Crear la boleta
        boleta_data = {
            'cliente': cliente.id,
            'fecha': datetime.now(),
            'cantidad': cantidad_total,
            'total': total,
        }
        print(f'Datos de boleta: {boleta_data}')
        boleta_serializer = BoletaSerializer(data=boleta_data, context={'ventas_en_carrito': ventas_en_carrito})
        if boleta_serializer.is_valid():
            # Guardar la boleta
            boleta = boleta_serializer.save()

            # Vaciar el carrito
            ventas_en_carrito.delete()

            return Response(boleta_serializer.data, status=status.HTTP_201_CREATED)
        
        print(f'Errores de serialización: {boleta_serializer.errors}')
        return Response(boleta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def obtener_boletas_con_venta(self, request):
        boletas = Boleta.objects.select_related('cliente').prefetch_related('boletaventa_set__venta').all()

        data = []
        for boleta in boletas:
            ventas_data = []
            for boleta_venta in boleta.boletaventa_set.all():
                venta = boleta_venta.venta
                venta_info = {
                    'id_venta': venta.id,
                    'marca': venta.marca,
                    'modelo': venta.modelo,
                    'estado': venta.estado,
                    'precio': venta.precio,
                    'anio': venta.anio,
                }
                ventas_data.append(venta_info)

            boleta_info = {
                'id_boleta': boleta.id,
                'fecha': boleta.fecha,
                'cantidad': boleta.cantidad,
                'total': boleta.total,
                'ventas': ventas_data,
                'cliente': {
                    'id_cliente': boleta.cliente.id if boleta.cliente else None,
                    'rut': boleta.cliente.rut if boleta.cliente else None,
                    'nombre': boleta.cliente.nombre if boleta.cliente else None,
                    'apellido': boleta.cliente.apellido if boleta.cliente else None,
                    'telefono': boleta.cliente.telefono if boleta.cliente else None,
                    'email': boleta.cliente.email if boleta.cliente else None,
                    'direccion': boleta.cliente.direccion if boleta.cliente else None
                }
            }
            data.append(boleta_info)

        return Response(data)

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


    @action(detail=False, methods=['post'])  # Accion personalizada para agregar al carrito
    def agregar_al_carrito(self, request):
        cliente_id = request.data.get('cliente_id')
        venta_id = request.data.get('venta_id')
        cantidad = int(request.data.get('cantidad', 1))
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        venta = get_object_or_404(Venta, pk=venta_id)
        carrito, created = Carrito.objects.get_or_create(cliente=cliente)
        carrito_venta, created = CarritoVenta.objects.get_or_create(carrito=carrito, venta=venta)
        if not created:
            carrito_venta.cantidad += cantidad
        else:
            carrito_venta.cantidad = cantidad
        carrito_venta.save()
        return Response({'status': 'success', 'message': 'Producto agregado al carrito'}, status=status.HTTP_200_OK)



    @action(detail=False, methods=['get'])
    def ver_carrito(self, request):
        cliente_id = request.query_params.get('cliente_id')
        if not cliente_id:
            return Response({'error': 'Se requiere el parámetro cliente_id en la solicitud.'}, status=status.HTTP_400_BAD_REQUEST)

        cliente = get_object_or_404(Cliente, pk=cliente_id)
        carrito = get_object_or_404(Carrito, cliente=cliente)
        ventas_en_carrito = CarritoVenta.objects.filter(carrito=carrito)

        carrito_data = []
        for item in ventas_en_carrito:
            carrito_data.append({
                'venta_id': item.venta.id,
                'marca': item.venta.marca,
                'modelo': item.venta.modelo,
                'cantidad': item.cantidad,
                'precio': item.venta.precio,
                'total': item.cantidad * item.venta.precio,
            })
        return Response({'carrito': carrito_data}, status=status.HTTP_200_OK)