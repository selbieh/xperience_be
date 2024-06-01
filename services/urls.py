from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarServiceViewSet, HotelServiceViewSet, HotelImageViewSet, CarImageViewSet, SubscriptionOptionViewSet

router = DefaultRouter()
router.register(r'car-services', CarServiceViewSet, basename="car_services")
router.register(r'hotel-services', HotelServiceViewSet, basename="hotel_services")
router.register(r'hotel-images', HotelImageViewSet, basename="hotel_images")
router.register(r'car-images', CarImageViewSet, basename="car_images")
router.register(r'subscription-option', SubscriptionOptionViewSet, basename="subscription_option")

urlpatterns = [
    path('', include(router.urls),),
]
