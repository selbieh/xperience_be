from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from .models import Reservation
from .serializers import ReservationSerializer, ReservationDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .filters import FilterReservation
from django.db.models import Sum, Count

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

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReservationDetailSerializer
        return ReservationSerializer

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
        payment_method = serializer.validated_data.get('payment_method')
        if payment_method in ['CREDIT_CARD']:
            status = 'WAITING_FOR_PAYMENT'
        if payment_method in ['POINTS', 'WALLET']:
            status = 'CONFIRMED'
        else:
            status = 'WAITING_FOR_CONFIRMATION'
        
        serializer.save(created_by=self.request.user, status=status)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        with transaction.atomic():
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class FilterReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterReservation

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        totals_qs = queryset.aggregate(
            total_final_price_car=Sum("car_reservations__final_price"),
            total_final_price_hotel=Sum("hotel_reservations__final_price"),
        )
        total_final_price_car = totals_qs["total_final_price_car"]
        total_final_price_hotel = totals_qs["total_final_price_hotel"]

        total_reservations = queryset.annotate(
            car_reservations_count=Count("car_reservations"),
            hotel_reservations_count=Count("hotel_reservations")
        )
        # Car Reservations
        car_reservations = total_reservations.values("car_reservations_count")
        total_car_reservations = sum(res['car_reservations_count'] for res in car_reservations)

        # Hotel Reservations
        hotel_reservations = total_reservations.values("hotel_reservations_count")
        total_hotel_reservations = sum(res['hotel_reservations_count'] for res in hotel_reservations)
        
        response = super().list(request, *args, **kwargs)
        count = response.data["count"]
        return Response(
            {
                "total_reservations": count,
                "total_final_price_car": total_final_price_car,
                "total_final_price_hotel": total_final_price_hotel,
                "total_car_reservations": total_car_reservations,
                "total_hotel_reservations": total_hotel_reservations,
            },
            status=status.HTTP_200_OK,
        )
