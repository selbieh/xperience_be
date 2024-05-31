from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarServiceViewSet, HotelServiceViewSet

router = DefaultRouter()
router.register(r'car-services', CarServiceViewSet, basename="car_services")
router.register(r'hotel-services', HotelServiceViewSet, basename="hotel_services")

urlpatterns = [
    path('', include(router.urls),),
]
