from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from .models import Reservation, Promocode
from .serializers import ReservationSerializer, ReservationDetailSerializer, PromocodeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .filters import FilterReservation
from django.db.models import Sum, Count

from rest_framework import serializers
from rest_framework.views import APIView
from django.utils import timezone
from services.models import ServiceOption

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
        if self.request.method in ['GET', 'POST', 'PATCH']:
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
        serializer.save(created_by=self.request.user)

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


class PromocodeViewSet(viewsets.ModelViewSet):
    queryset = Promocode.objects.all()
    serializer_class = PromocodeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]




class CalculateReservationView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ReservationSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            try:
                response_data = self.calculate_reservation(serializer.validated_data, request.user)
                return Response(response_data, status=status.HTTP_200_OK)
            except serializers.ValidationError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def calculate_reservation(self, validated_data, user):
        # Perform the calculations here without saving to the database
        car_reservations_data = validated_data.get('car_reservations', [])
        hotel_reservations_data = validated_data.get('hotel_reservations', [])
        payment_method = validated_data.get('payment_method')
        promocode_code = validated_data.get('promocode', None)

        total_price = 0
        total_points_price = 0
        discount = 0

        # Apply promocode if provided
        promocode = None
        if promocode_code:
            try:
                promocode = Promocode.objects.get(code=promocode_code, is_active=True)
                if promocode.expiration_date and promocode.expiration_date < timezone.now():
                    raise serializers.ValidationError("Promocode has expired.")
            except Promocode.DoesNotExist:
                raise serializers.ValidationError("Invalid promocode.")

        # Calculate car reservations
        car_reservations = []
        for car_reservation_data in car_reservations_data:
            options_data = car_reservation_data.pop('options', [])
            subscription_option = car_reservation_data.get('subscription_option')

            car_final_price = 0
            car_final_points_price = 0
            if subscription_option:
                car_final_price += subscription_option.price
                if payment_method == 'POINTS' and not subscription_option.points_price:
                    raise serializers.ValidationError("This reservation cannot be completed with points.")
                car_final_points_price += subscription_option.points_price if subscription_option.points_price else 0

            car_options = []
            for option_data in options_data:
                service_option = ServiceOption.objects.get(id=option_data['service_option'].id)
                quantity = option_data['quantity']
                if quantity > service_option.max_free:
                    car_final_price += (quantity - service_option.max_free) * service_option.price
                    if payment_method == 'POINTS' and not service_option.points_price:
                        raise serializers.ValidationError("This reservation cannot be completed with points.")
                    car_final_points_price += (quantity - service_option.max_free) * service_option.points_price if service_option.points_price else 0
                car_options.append({
                    "service_option": service_option.id,
                    "service_option_name": service_option.name,
                    "quantity": quantity,
                    "price": service_option.price,
                    "max_free": service_option.max_free,
                    "points_price": service_option.points_price
                })

            total_price += car_final_price
            total_points_price += car_final_points_price
            car_reservations.append({
                "car_service": car_reservation_data.get('car_service_id'),
                "pickup_time": car_reservation_data.get('pickup_time'),
                "pickup_address": car_reservation_data.get('pickup_address'),
                "dropoff_address": car_reservation_data.get('dropoff_address'),
                "terminal": car_reservation_data.get('terminal'),
                "flight_number": car_reservation_data.get('flight_number'),
                "extras": car_reservation_data.get('extras'),
                "final_price": car_final_price,
                "subscription_option": subscription_option.id if subscription_option else None,
                "subscription_option_price": subscription_option.price if subscription_option else None,
                "options": car_options
            })

        # Calculate hotel reservations
        hotel_reservations = []
        for hotel_reservation_data in hotel_reservations_data:
            options_data = hotel_reservation_data.pop('options', [])
            hotel_service = hotel_reservation_data.get('hotel_service')

            check_in_date = hotel_reservation_data.get('check_in_date')
            check_out_date = hotel_reservation_data.get('check_out_date')
            num_days = (check_out_date - check_in_date).days

            hotel_final_price = num_days * hotel_service.day_price
            if payment_method == 'POINTS' and not hotel_service.points_price:
                raise serializers.ValidationError("This reservation cannot be completed with points.")
            hotel_final_points_price = num_days * hotel_service.points_price if hotel_service.points_price else 0

            hotel_options = []
            for option_data in options_data:
                service_option = ServiceOption.objects.get(id=option_data['service_option'].id)
                quantity = option_data['quantity']
                if quantity > service_option.max_free:
                    hotel_final_price += (quantity - service_option.max_free) * service_option.price
                    if payment_method == 'POINTS' and not service_option.points_price:
                        raise serializers.ValidationError("This reservation cannot be completed with points.")
                    hotel_final_points_price += (quantity - service_option.max_free) * service_option.points_price if service_option.points_price else 0
                hotel_options.append({
                    "service_option": service_option.id,
                    "service_option_name": service_option.name,
                    "quantity": quantity,
                    "price": service_option.price,
                    "max_free": service_option.max_free,
                    "points_price": service_option.points_price
                })

            total_price += hotel_final_price
            total_points_price += hotel_final_points_price
            hotel_reservations.append({
                "hotel_service": hotel_service.id,
                "hotel_service_price": hotel_service.day_price,
                "check_in_date": hotel_reservation_data.get('check_in_date'),
                "check_out_date": hotel_reservation_data.get('check_out_date'),
                "extras": hotel_reservation_data.get('extras'),
                "final_price": hotel_final_price,
                "options": hotel_options
            })

        # Apply promocode discount
        if promocode:
            if promocode.discount_type == 'PERCENTAGE':
                discount = total_price * (promocode.discount_value / 100)
            elif promocode.discount_type == 'FIXED':
                discount = promocode.discount_value
            total_price -= discount

        response_data = {
            "car_reservations": car_reservations,
            "hotel_reservations": hotel_reservations,
            "status": "WAITING_FOR_PAYMENT" if payment_method == 'CREDIT_CARD' else "PENDING",
            "payment_method": payment_method,
            "promocode": promocode.code if promocode else None,
            "discount": discount,
            "final_reservation_price": total_price,
            "total_points_price": total_points_price
        }

        return response_data
