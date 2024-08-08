from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.filters import SearchFilter
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import CarService, HotelService, HotelImage, CarImage, SubscriptionOption, ServiceOption, HotelServiceFeature, CarModel, CarMake
from .serializers import (
    CarServiceListSerializer, CarServiceDetailSerializer, 
    HotelServiceListSerializer, HotelServiceDetailSerializer, HotelImageSerializer, CarImageSerializer, SubscriptionOptionSerializer,
    ServiceOptionSerializer, HotelServiceFeatureSerializer, CarMakeSerializer, CarModelSerializer, SubscriptionOptionWriteSerializer
)

class CarServiceViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['type', 'color']
    filterset_fields = ['model', 'make']

    def get_queryset(self):
        if self.request.user.is_staff:
            return CarService.objects.select_related('make', 'model').all()
        return CarService.objects.select_related('make', 'model').filter(active=True)

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


class HotelServiceFilter(django_filters.FilterSet):
    availability_start_gte = django_filters.DateFilter(field_name='availability_start', lookup_expr='lte')
    availability_end_lte = django_filters.DateFilter(field_name='availability_end', lookup_expr='gte')

    class Meta:
        model = HotelService
        fields = ['features__id', 'address']


class HotelServiceViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'address']
    filterset_class = HotelServiceFilter

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
    filterset_fields = ['type', 'car_service']

    def get_permissions(self):
        if self.request.method in ['GET']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return SubscriptionOptionWriteSerializer
        return SubscriptionOptionSerializer


class ServiceOptionViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceOptionSerializer
    filterset_fields = ['service_type', 'type']

    def get_queryset(self):
        if self.request.user.is_staff:
            return ServiceOption.objects.all()
        return ServiceOption.objects.filter(active=True)
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class HotelServiceFeatureViewSet(viewsets.ModelViewSet):
    queryset = HotelServiceFeature.objects.all()
    serializer_class = HotelServiceFeatureSerializer
    def get_permissions(self):
        if self.request.method in ['GET']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CarMakeViewSet(viewsets.ModelViewSet):
    queryset = CarMake.objects.all()
    serializer_class = CarMakeSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['name']

    def get_permissions(self):
        if self.request.method in ['GET']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['name', 'make']

    def get_permissions(self):
        if self.request.method in ['GET']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
