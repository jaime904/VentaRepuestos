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
        serializer = VentaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#comenta para que sirve este codigo y que hace
#Este código es un ViewSet que se encarga de manejar las peticiones HTTP de la entidad Venta.
#Se encarga de manejar las peticiones de tipo GET, POST, PUT, DELETE y PATCH.
#Además, se define un método create_venta que se encarga de crear una nueva venta.
#Este método se encarga de recibir los datos de la venta, validarlos y guardarlos en la base de datos.
#Si los datos son válidos, se retorna un código de estado 201 (CREATED) y los datos de la venta creada.