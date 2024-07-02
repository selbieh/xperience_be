from rest_framework import serializers
from django.db import transaction
from users.models import User
from .models import (
    Reservation, CarReservation, HotelReservation,
    CarReservationOption, HotelReservationOption, ServiceOption, SubscriptionOption
)
from users.serializers import UserProfileSerializer
from datetime import timedelta
from services.serializers import CarServiceMinimalSerializer, HotelServiceMinimalSerializer
from services.models import CarService, HotelService

class CarReservationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarReservationOption
        fields = ['service_option', 'quantity']

class CarReservationSerializer(serializers.ModelSerializer):
    options = CarReservationOptionSerializer(many=True)
    car_service = serializers.SerializerMethodField()
    car_service_id = serializers.PrimaryKeyRelatedField(
        queryset=CarService.objects.all(), 
        write_only=True, 
        source='car_service'
    )

    def get_car_service(self, obj):
        return CarServiceMinimalSerializer(obj.car_service).data

    class Meta:
        model = CarReservation
        fields = [
            'id', 'car_service_id', 'car_service', 'pickup_time', 'pickup_address', 'pickup_lat', 'pickup_long', 'pickup_url',
            'dropoff_address', 'dropoff_lat', 'dropoff_long', 'dropoff_url', 'terminal', 'flight_number',
            'extras', 'final_price', 'subscription_option', 'options'
        ]

class HotelReservationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReservationOption
        fields = ['service_option', 'quantity']

class HotelReservationSerializer(serializers.ModelSerializer):
    options = HotelReservationOptionSerializer(many=True)
    hotel_service = serializers.SerializerMethodField()
    hotel_service_id = serializers.PrimaryKeyRelatedField(
        queryset=HotelService.objects.all(), 
        write_only=True, 
        source='hotel_service'
    )

    def get_hotel_service(self, obj):
        return HotelServiceMinimalSerializer(obj.hotel_service).data

    class Meta:
        model = HotelReservation
        fields = [
            'id', 'hotel_service_id', 'hotel_service', 'check_in_date', 'check_out_date', 'extras', 'final_price', 'options'
        ]

class ReservationSerializer(serializers.ModelSerializer):
    car_reservations = CarReservationSerializer(many=True, required=False)
    hotel_reservations = HotelReservationSerializer(many=True, required=False)
    created_by = UserProfileSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    user_details = UserProfileSerializer(source='user', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'user_details', 'car_reservations', 'hotel_reservations', 'created_by', 'status', 'created_at']

    def validate(self, data):
        if self.instance is None:
            car_reservations = data.get('car_reservations', None)
            hotel_reservations = data.get('hotel_reservations', None)
            if not car_reservations and not hotel_reservations:
                raise serializers.ValidationError("At least one CarReservation or HotelReservation is required.")
        return data

    def create(self, validated_data):
        car_reservations_data = validated_data.pop('car_reservations', [])
        hotel_reservations_data = validated_data.pop('hotel_reservations', [])

        with transaction.atomic():
            reservation = Reservation.objects.create(**validated_data)

            # Create Car Reservations
            for car_reservation_data in car_reservations_data:
                options_data = car_reservation_data.pop('options')
                subscription_option = car_reservation_data.get('subscription_option')
                total_price = 0

                # Calculate the price of the subscription option if it exists
                if subscription_option:
                    total_price += subscription_option.price

                car_reservation = CarReservation.objects.create(reservation=reservation, **car_reservation_data)
                
                for option_data in options_data:
                    service_option = ServiceOption.objects.get(id=option_data['service_option'].id)
                    quantity = option_data['quantity']
                    if quantity > service_option.max_free:
                        total_price += (quantity - service_option.max_free) * service_option.price
                    CarReservationOption.objects.create(car_reservation=car_reservation, **option_data)
                
                car_reservation.final_price = total_price
                car_reservation.save()

            # Create Hotel Reservations
            for hotel_reservation_data in hotel_reservations_data:
                options_data = hotel_reservation_data.pop('options')
                hotel_reservation = HotelReservation.objects.create(reservation=reservation, **hotel_reservation_data)
                
                # Calculate the total price based on the number of days
                check_in_date = hotel_reservation.check_in_date
                check_out_date = hotel_reservation.check_out_date
                num_days = (check_out_date - check_in_date).days
                total_price = num_days * hotel_reservation.hotel_service.day_price
                
                for option_data in options_data:
                    service_option = ServiceOption.objects.get(id=option_data['service_option'].id)
                    quantity = option_data['quantity']
                    if quantity > service_option.max_free:
                        total_price += (quantity - service_option.max_free) * service_option.price
                    HotelReservationOption.objects.create(hotel_reservation=hotel_reservation, **option_data)
                
                hotel_reservation.final_price = total_price
                hotel_reservation.save()

        return reservation
