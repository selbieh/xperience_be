from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarServiceViewSet, HotelServiceViewSet, HotelImageViewSet, CarImageViewSet, SubscriptionOptionViewSet, ServiceOptionViewSet, HotelServiceFeatureViewSet

router = DefaultRouter()
router.register(r'car-services', CarServiceViewSet, basename="car_services")
router.register(r'hotel-services', HotelServiceViewSet, basename="hotel_services")
router.register(r'hotel-images', HotelImageViewSet, basename="hotel_images")
router.register(r'car-images', CarImageViewSet, basename="car_images")
router.register(r'subscription-options', SubscriptionOptionViewSet, basename="subscription_options")
router.register(r'service-options', ServiceOptionViewSet, basename="service_options")
router.register(r'hotel-service-features', HotelServiceFeatureViewSet, basename="hotel_service_features")

urlpatterns = [
    path('', include(router.urls),),
]
