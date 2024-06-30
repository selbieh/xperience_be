from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

class ReservationFilter(filters.FilterSet):
    has_car_reservations = filters.BooleanFilter(method='filter_car_reservations')
    has_hotel_reservations = filters.BooleanFilter(method='filter_hotel_reservations')

    class Meta:
        model = Reservation
        fields = ['status', 'has_car_reservations', 'has_hotel_reservations']

    def filter_car_reservations(self, queryset, name, value):
        if value:
            return queryset.filter(car_reservations__isnull=False).distinct()
        return queryset.filter(car_reservations__isnull=True).distinct()

    def filter_hotel_reservations(self, queryset, name, value):
        if value:
            return queryset.filter(hotel_reservations__isnull=False).distinct()
        return queryset.filter(hotel_reservations__isnull=True).distinct()

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['user__mobile', 'created_by__name']
    filterset_class = ReservationFilter

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.all().order_by("-created_at")
        return Reservation.objects.filter(user=user).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_staff:
            serializer.validated_data['user'] = request.user

        with transaction.atomic():
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, status='CONFIRMED')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        with transaction.atomic():
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

