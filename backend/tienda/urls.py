from django.contrib import admin
from django.urls import path, include
from venta.api import VentaViewSet
from rest_framework.routers import DefaultRouter

# Creamos un router para la vista VentaViewSet
router = DefaultRouter()
router.register(r'venta', VentaViewSet, basename='venta')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # Incluimos las URLs del router
]
