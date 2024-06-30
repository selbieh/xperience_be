from django_filters import rest_framework as filters

from .models import Reservation, CarReservation
from services.models import HotelServiceFeature


class filter_by_car_reservation(filters.FilterSet):
    class Meta:
        model = CarReservation
        fields = ["car_service"]

    def filter_by_car_reservation(self, queryset, name, value):
        return True


class FilterReservation(filters.FilterSet):
    # Car Service
    model = filters.CharFilter(
        field_name="car_reservations__car_service__model__name", lookup_expr="icontains"
    )
    make = filters.CharFilter(
        field_name="car_reservations__car_service__make__name", lookup_expr="icontains"
    )
    car_subscription_type = filters.BooleanFilter(
        field_name="car_reservations__subscription_option__type"
    )
    car_subscription_duration = filters.NumberFilter(
        field_name="car_reservations__subscription_option__duration_hours"
    )
    
    # Hotel Service
    number_of_rooms = filters.NumberFilter(
        field_name='hotel_reservations__number_of_rooms'
    )
    number_of_rooms = filters.NumberFilter(
        field_name='hotel_reservations__number_of_beds'
    )
    features = filters.ModelMultipleChoiceFilter(
        field_name='hotel_reservations__features__id',
        queryset=HotelServiceFeature.objects.all()
    )

    class Meta:
        model = Reservation
        fields = ["status", "user", "created_by", "model", "make"]
