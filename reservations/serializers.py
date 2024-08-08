from rest_framework import serializers
from django.db import transaction
from users.models import User
from .models import (
    Reservation, CarReservation, HotelReservation,
    CarReservationOption, HotelReservationOption, ServiceOption, SubscriptionOption, Promocode
)
from users.serializers import UserProfileSerializer
from datetime import timedelta
from services.serializers import CarServiceMinimalSerializer, HotelServiceMinimalSerializer
from services.models import CarService, HotelService
from django.utils import timezone
from .signals import send_reservation_notifications

class CarReservationOptionSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    max_free = serializers.SerializerMethodField()
    points_price = serializers.SerializerMethodField()

    class Meta:
        model = CarReservationOption
        fields = ['service_option', 'quantity', 'price', 'max_free', 'points_price']

    def get_price(self, obj):
        service_option = obj.service_option
        quantity = obj.quantity
        if quantity > service_option.max_free:
            return (quantity - service_option.max_free) * service_option.price
        return 0
    
    def get_max_free(self, obj):
        service_option = obj.service_option
        return service_option.max_free
    
    def get_points_price(self, obj):
        service_option = obj.service_option
        return service_option.points_price
class CarReservationSerializer(serializers.ModelSerializer):
    options = CarReservationOptionSerializer(many=True)
    car_service = serializers.SerializerMethodField()
    car_service_id = serializers.PrimaryKeyRelatedField(
        queryset=CarService.objects.all(), 
        write_only=True, 
        source='car_service'
    )
    subscription_option = serializers.IntegerField()

    def validate_subscription_option(self, value):
        car_service_id = self.data.get('car_service_id')
        if car_service_id is None:
            raise serializers.ValidationError("You Should Choose a duration option.")
        if not SubscriptionOption.objects.filter(car_service=car_service_id).exists():
            raise serializers.ValidationError("Duration option is not associated with the choosen car service.") 
        return value
    
    def get_car_service(self, obj):
        return CarServiceMinimalSerializer(obj.car_service).data

    class Meta:
        model = CarReservation
        fields = [
            'id', 'car_service_id', 'car_service', 'pickup_time', 'pickup_address', 'pickup_lat', 'pickup_long', 'pickup_url',
            'dropoff_address', 'dropoff_lat', 'dropoff_long', 'dropoff_url', 'terminal', 'flight_number',
            'extras', 'final_price', 'subscription_option', 'options'
        ]
        read_only_fields=["final_price"]

class HotelReservationOptionSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    max_free = serializers.SerializerMethodField()
    points_price = serializers.SerializerMethodField()
    class Meta:
        model = HotelReservationOption
        fields = ['service_option', 'quantity', 'price', "max_free", "points_price"]

    def get_price(self, obj):
        service_option = obj.service_option
        quantity = obj.quantity
        if quantity > service_option.max_free:
            return (quantity - service_option.max_free) * service_option.price
        return 0

    def get_max_free(self, obj):
        service_option = obj.service_option
        return service_option.max_free
    
    def get_points_price(self, obj):
        service_option = obj.service_option
        return service_option.points_price

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
        read_only_fields=["final_price"]

class ReservationSerializer(serializers.ModelSerializer):
    car_reservations = CarReservationSerializer(many=True, required=False)
    hotel_reservations = HotelReservationSerializer(many=True, required=False)
    created_by = UserProfileSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    promocode = serializers.CharField(required=False, allow_blank=True)
    discount = serializers.SerializerMethodField()
    final_reservation_price = serializers.SerializerMethodField()
    final_reservation_price = serializers.SerializerMethodField()
    total_points_price = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'car_reservations', 'hotel_reservations', 'created_by', 'status', 'created_at', 'payment_method', 'promocode', 'discount', "final_reservation_price", "total_points_price"]

    def get_total_price(self, obj):
        total_price = 0
        car_reservations = obj.car_reservations.all()
        hotel_reservations = obj.hotel_reservations.all()
        for cr in car_reservations:
            total_price += cr.final_price or 0
        for hr in hotel_reservations:
            total_price += hr.final_price or 0
        return total_price
    
    def get_discount(self, obj):
        discount = 0
        if obj.promocode:
            total_price = self.get_total_price(obj)
            if obj.promocode.discount_type == 'PERCENTAGE':
                discount = total_price * (obj.promocode.discount_value / 100)
            elif obj.promocode.discount_type == 'FIXED':
                discount = obj.promocode.discount_value
            else: 
                discount=0
        return discount    
    
    def get_final_reservation_price(self, obj):
        total_price = self.get_total_price(obj)
        discount = self.get_discount(obj)
        return total_price - discount

    def get_total_points_price(self, obj):
        total_points_price = 0
        car_reservations = obj.car_reservations.all()
        hotel_reservations = obj.hotel_reservations.all()
        for cr in car_reservations:
            total_points_price += cr.final_points_price or 0
        for hr in hotel_reservations:
            total_points_price += hr.final_points_price or 0
        return total_points_price

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

            user = self.context['request'].user
            payment_method = validated_data.get('payment_method')
            total_price = 0
            total_points_price = 0
            promocode_code = validated_data.pop('promocode', None)
            car_reservation = None
            hotel_reservation = None

            promocode = None
            if promocode_code:
                try:
                    promocode = Promocode.objects.get(code=promocode_code, is_active=True)
                    if promocode.expiration_date and promocode.expiration_date < timezone.now():
                        raise serializers.ValidationError("Promocode has expired.")
                except Promocode.DoesNotExist:
                    raise serializers.ValidationError("Invalid promocode.")
                
            with transaction.atomic():
                # Create Car Reservations
                reservation = Reservation.objects.create(**validated_data)
                if promocode:
                    reservation.promocode = promocode
                    reservation.save()

                for car_reservation_data in car_reservations_data:
                    options_data = car_reservation_data.pop('options', [])
                    subscription_option = car_reservation_data.get('subscription_option')

                    if subscription_option:
                        total_price += subscription_option.price
                        if payment_method == 'POINTS' and not subscription_option.points_price:
                            raise serializers.ValidationError("This reservation cannot be completed with points.")
                        total_points_price += subscription_option.points_price if subscription_option.points_price else 0

                    car_reservation = CarReservation.objects.create(reservation=reservation, **car_reservation_data)
                    
                    for option_data in options_data:
                        service_option = ServiceOption.objects.get(id=option_data['service_option'].id)
                        quantity = option_data['quantity']
                        if quantity > service_option.max_free:
                            total_price += (quantity - service_option.max_free) * service_option.price
                            if payment_method == 'POINTS' and not service_option.points_price:
                                raise serializers.ValidationError("This reservation cannot be completed with points.")
                            total_points_price += (quantity - service_option.max_free) * service_option.points_price if service_option.points_price else 0
                        CarReservationOption.objects.create(car_reservation=car_reservation, **option_data)
                    
                    car_reservation.final_price = total_price
                    car_reservation.final_points_price = total_points_price
                    car_reservation.save()

                total_price=0
                total_points_price=0
                # Create Hotel Reservations
                for hotel_reservation_data in hotel_reservations_data:
                    options_data = hotel_reservation_data.pop('options', [])
                    hotel_service = hotel_reservation_data.get('hotel_service')

                    # Check if the reservation dates are within the available dates
                    check_in_date = hotel_reservation_data.get('check_in_date')
                    check_out_date = hotel_reservation_data.get('check_out_date')
                    if (hotel_service.availability_start and check_in_date < hotel_service.availability_start) or \
                    (hotel_service.availability_end and check_out_date > hotel_service.availability_end):
                        raise serializers.ValidationError("The reservation dates are outside the available dates for this hotel service.")
                    
                    hotel_reservation = HotelReservation.objects.create(reservation=reservation, **hotel_reservation_data)
                    
                    check_in_date = hotel_reservation.check_in_date
                    check_out_date = hotel_reservation.check_out_date
                    num_days = (check_out_date - check_in_date).days
                    if num_days <= 0:
                        raise serializers.ValidationError("The checkout date must be at least one day after the check-in date. Please provide a valid date range.")
                    total_price += num_days * hotel_reservation.hotel_service.day_price
                    if payment_method == 'POINTS' and not hotel_reservation.hotel_service.points_price:
                        raise serializers.ValidationError("This reservation cannot be completed with points.")
                    total_points_price += num_days * hotel_reservation.hotel_service.points_price if hotel_reservation.hotel_service.points_price else 0
                    
                    for option_data in options_data:
                        service_option = ServiceOption.objects.get(id=option_data['service_option'].id)
                        quantity = option_data['quantity']
                        if quantity > service_option.max_free:
                            total_price += (quantity - service_option.max_free) * service_option.price
                            if payment_method == 'POINTS' and not service_option.points_price:
                                raise serializers.ValidationError("This reservation cannot be completed with points.")
                            total_points_price += (quantity - service_option.max_free) * service_option.points_price if service_option.points_price else 0
                        HotelReservationOption.objects.create(hotel_reservation=hotel_reservation, **option_data)
                    
                    hotel_reservation.final_price = total_price
                    hotel_reservation.final_points_price = total_points_price
                    hotel_reservation.save()
                

                # Apply promocode if provided
                discount = 0
                if promocode_code:
                    try:
                        promocode = Promocode.objects.get(code=promocode_code, is_active=True)
                        if promocode.expiration_date and promocode.expiration_date < timezone.now():
                            raise serializers.ValidationError("Promocode has expired.")
                        if promocode.discount_type == 'PERCENTAGE':
                            discount = total_price * (promocode.discount_value / 100)
                            reservation.promocode=promocode
                        elif promocode.discount_type == 'FIXED':
                            discount = promocode.discount_value
                            reservation.promocode = promocode
                        validated_data['promocode'] = promocode
                    except Promocode.DoesNotExist:
                        raise serializers.ValidationError("Invalid promocode.")


                total_price=0
                if car_reservation:
                    total_price += car_reservation.final_price
                if hotel_reservation:
                    total_price += hotel_reservation.final_price
                if promocode:
                    total_price -= discount


                total_points_price=0
                if car_reservation:
                    total_points_price += car_reservation.final_points_price
                if hotel_reservation:
                    total_points_price += hotel_reservation.final_points_price
                if promocode:
                    total_points_price

                # Handle payment method
                if payment_method == 'CREDIT_CARD':
                    reservation.status = 'WAITING_FOR_PAYMENT'
                elif payment_method == 'WALLET':
                    if user.wallet < total_price:
                        raise serializers.ValidationError("You don't have enogh wallet balance.")
                    user.wallet -= total_price
                    user.save()
                    reservation.status = 'PAID'
                elif payment_method == 'POINTS':
                    if user.points < total_points_price:
                        raise serializers.ValidationError("You don't have enogh points.")
                    user.points -= total_points_price
                    user.save()
                    reservation.status = 'PAID'
                else:  # For POS and Cash on Delivery
                    reservation.status = 'WAITING_FOR_CONFIRMATION'

                reservation.save()
                send_reservation_notifications(reservation, created=False)
            return reservation
    
    def update(self, instance, validated_data):
        previous_status = instance.status  # Capture the previous status

        # Use the default update behavior
        updated_instance = super().update(instance, validated_data)

        # Check if the status has changed and send a notification
        current_status = updated_instance.status
        if current_status != previous_status:
            send_reservation_notifications(updated_instance, created=False)

        return updated_instance

class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = ['id', 'code', 'discount_type', 'discount_value', 'is_active', 'expiration_date']


# class ReservationDetailSerializer(serializers.ModelSerializer):
#     car_reservations = CarReservationSerializer(many=True, read_only=True)
#     hotel_reservations = HotelReservationSerializer(many=True, read_only=True)
#     created_by = UserProfileSerializer(read_only=True)
#     user = UserProfileSerializer(read_only=True)  # Include user details
#     promocode = PromocodeSerializer()

#     class Meta:
#         model = Reservation
#         fields = ['id', 'user', 'car_reservations', 'hotel_reservations', 'created_by', 'status', 'created_at', 'payment_method', 'promocode']


class ReservationDetailSerializer(serializers.ModelSerializer):
    car_reservations = CarReservationSerializer(many=True, read_only=True)
    hotel_reservations = HotelReservationSerializer(many=True, read_only=True)
    created_by = UserProfileSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)  # Include user details
    promocode = PromocodeSerializer()
    discount = serializers.SerializerMethodField()
    final_reservation_price = serializers.SerializerMethodField()
    total_points_price = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'car_reservations', 'hotel_reservations', 
            'created_by', 'status', 'created_at', 'payment_method', 
            'promocode', 'discount', 'final_reservation_price', 'total_points_price'
        ]

    def get_total_price(self, obj):
        total_price = 0
        car_reservations = obj.car_reservations.all()
        hotel_reservations = obj.hotel_reservations.all()
        for cr in car_reservations:
            total_price += cr.final_price or 0
        for hr in hotel_reservations:
            total_price += hr.final_price or 0
        return total_price

    def get_discount(self, obj):
        discount = 0
        if obj.promocode:
            total_price = self.get_total_price(obj)
            if obj.promocode.discount_type == 'PERCENTAGE':
                discount = total_price * (obj.promocode.discount_value / 100)
            elif obj.promocode.discount_type == 'FIXED':
                discount = obj.promocode.discount_value
        return discount

    def get_final_reservation_price(self, obj):
        total_price = self.get_total_price(obj)
        discount = self.get_discount(obj)
        return total_price - discount

    def get_total_points_price(self, obj):
        total_points_price = 0
        car_reservations = obj.car_reservations.all()
        hotel_reservations = obj.hotel_reservations.all()
        for cr in car_reservations:
            total_points_price += cr.final_points_price or 0
        for hr in hotel_reservations:
            total_points_price += hr.final_points_price or 0
        return total_points_price
