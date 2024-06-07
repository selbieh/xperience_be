from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.filters import SearchFilter
from .models import CarService, HotelService, HotelImage, CarImage, SubscriptionOption, ServiceOption
from .serializers import (
    CarServiceListSerializer, CarServiceDetailSerializer, 
    HotelServiceListSerializer, HotelServiceDetailSerializer, HotelImageSerializer, CarImageSerializer, SubscriptionOptionSerializer,
    ServiceOptionSerializer
)

class CarServiceViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['model', 'make', 'type']
    filterset_fields = ['model', 'make', 'year', 'color', 'type', 'number_of_seats', 'cool']

    def get_queryset(self):
        if self.request.user.is_staff:
            return CarService.objects.all()
        return CarService.objects.filter(active=True)

    def get_serializer_class(self):
        if self.action in ['list']:
            return CarServiceListSerializer
        return CarServiceDetailSerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class HotelServiceViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['name', 'address']
    filterset_fields = ['day_price']

    def get_queryset(self):
        if self.request.user.is_staff:
            return HotelService.objects.all()
        return HotelService.objects.filter(active=True)

    def get_serializer_class(self):
        if self.action in ['list']:
            return HotelServiceListSerializer
        return HotelServiceDetailSerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    

class HotelImageViewSet(viewsets.ModelViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['hotel_service']


class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['car_service']


class SubscriptionOptionViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionOption.objects.all()
    serializer_class = SubscriptionOptionSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['type', 'car_service']


class ServiceOptionViewSet(viewsets.ModelViewSet):
    queryset = ServiceOption.objects.all()
    serializer_class = ServiceOptionSerializer
    filterset_fields = ['service_type', 'type']

    def get_permissions(self):
        if self.request.method in ['GET']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

