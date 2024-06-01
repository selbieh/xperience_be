from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import CarService, HotelService, HotelImage, CarImage, SubscriptionOption
from .serializers import (
    CarServiceListSerializer, CarServiceDetailSerializer, 
    HotelServiceListSerializer, HotelServiceDetailSerializer, HotelImageSerializer, CarImageSerializer, SubscriptionOptionSerializer
)

class CarServiceViewSet(viewsets.ModelViewSet):
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


class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    permission_classes = [IsAdminUser]


class SubscriptionOptionViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionOption.objects.all()
    serializer_class = SubscriptionOptionSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['type'] 

