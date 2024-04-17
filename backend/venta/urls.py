from rest_framework import routers
from .api import VentaViewSet

router = routers.DefaultRouter()

router.register('api/venta', VentaViewSet, 'venta')

urlpatterns = router.urls