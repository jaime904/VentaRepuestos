from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Venta
from .serializers import VentaSerializer
from rest_framework.decorators import action 

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    permission_classes = [AllowAny] 
    serializer_class = VentaSerializer

    @action(detail=False, methods=['post'])
    def create_venta(self, request):
        data_nueva = request.data
        print("hola")
        data_nueva['estado'] = True
        print("hola2")
        serializer = VentaSerializer(data=data_nueva)
        print("hola3")
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response({'detail': 'Los datos proporcionados son inválidos.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail = False, methods=['get']	)
    def devolverListado(self, request):
        queryset = Venta.objects.all()
        serializer = self.get_serializer(queryset, many = True)
        print(serializer.data)
        return Response(serializer.data, status = status.HTTP_200_OK)
    

#comenta para que sirve este codigo y que hace
#Este código es un ViewSet que se encarga de manejar las peticiones HTTP de la entidad Venta.
#Se encarga de manejar las peticiones de tipo GET, POST, PUT, DELETE y PATCH.
#Además, se define un método create_venta que se encarga de crear una nueva venta.
#Este método se encarga de recibir los datos de la venta, validarlos y guardarlos en la base de datos.
#Si los datos son válidos, se retorna un código de estado 201 (CREATED) y los datos de la venta creada.
#Si los datos no son válidos, se retorna un código de estado 400 (BAD REQUEST) y los errores de validación.
#Este código también define la clase VentaViewSet que se encarga de manejar las peticiones HTTP de la entidad Venta.
#Se define el queryset como todos los objetos de la entidad Venta.
#Se define la clase de serializador como VentaSerializer.