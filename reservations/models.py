from django.db import models
from base.models import AbstractBaseModel
from django.conf import settings
from services.models import ServiceOption, HotelService, CarService, SubscriptionOption

class Reservation(AbstractBaseModel):
    STATUS_CHOICES = [
        ('WAITING_FOR_PAYMENT', 'Waiting for Payment'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('CREDIT_CARD', 'Credit Card'),
        ('WALLET', 'Wallet'),
        ('CASH_ON_DELIVERY', 'Cash on Delivery'),
        ('CAR_POS', 'Car Point of Sale'),
        ('POINTS', 'Points')
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WAITING_FOR_PAYMENT')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_reservations')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='CASH_ON_DELIVERY')


class CarReservation(AbstractBaseModel):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='car_reservations')
    car_service = models.ForeignKey(CarService, on_delete=models.CASCADE, related_name='car_reservations')
    subscription_option = models.ForeignKey(SubscriptionOption, null=True, on_delete=models.SET_NULL, related_name='car_reservations')
    pickup_time = models.DateTimeField()
    pickup_address = models.CharField(max_length=255)
    pickup_lat = models.FloatField(null=True, blank=True)
    pickup_long = models.FloatField(null=True, blank=True)
    pickup_url = models.URLField(max_length=500, null=True, blank=True)
    dropoff_address = models.CharField(max_length=255)
    dropoff_lat = models.FloatField(null=True, blank=True)
    dropoff_long = models.FloatField(null=True, blank=True)
    dropoff_url = models.URLField(max_length=500, null=True, blank=True)
    terminal = models.CharField(max_length=100, null=True, blank=True)
    flight_number = models.CharField(max_length=100, null=True, blank=True)
    extras = models.TextField(null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class CarReservationOption(AbstractBaseModel):
    car_reservation = models.ForeignKey(CarReservation, on_delete=models.CASCADE, related_name='options')
    service_option = models.ForeignKey(ServiceOption, on_delete=models.CASCADE, related_name='car_reservation_options')
    quantity = models.IntegerField()


class HotelReservation(AbstractBaseModel):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='hotel_reservations')
    hotel_service = models.ForeignKey(HotelService, on_delete=models.CASCADE, related_name='hotel_reservations')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    extras = models.TextField(null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class HotelReservationOption(AbstractBaseModel):
    hotel_reservation = models.ForeignKey(HotelReservation, on_delete=models.CASCADE, related_name='options')
    service_option = models.ForeignKey(ServiceOption, on_delete=models.CASCADE, related_name='hotel_reservation_options')
    quantity = models.IntegerField()





