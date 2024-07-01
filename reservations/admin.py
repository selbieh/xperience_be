from django.contrib import admin
from .models import Reservation, CarReservation, HotelReservation, HotelReservationOption, CarReservationOption
# Register your models here.

admin.site.register(Reservation)
admin.site.register(CarReservation)
admin.site.register(CarReservationOption)
admin.site.register(HotelReservation)
admin.site.register(HotelReservationOption)