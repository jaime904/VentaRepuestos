from rest_framework import routers
from .api import VentaViewSet

router = routers.DefaultRouter()

router.register('api/venta', VentaViewSet, 'venta')

# Registra la acción personalizada obtener_boletas_con_venta

urlpatterns = router.urls
#comenta para que sirve este codigo y que hace  
#Este código define las rutas de la API de la aplicación Venta.
#Se importa el módulo routers de rest_framework y la clase VentaViewSet del módulo api.
#Se crea un enrutador por defecto llamado router.
#Se registra la ruta 'api/venta' con el ViewSet VentaViewSet y el nombre 'venta'.
#Se definen las rutas de la API con router.urls.
#Esto permite acceder a las vistas de la API de la entidad Venta a través de las rutas definidas en este archivo.