from django_filters import rest_framework as filters

from .models import Reservation, CarReservation, SubscriptionOption
from services.models import HotelServiceFeature


class filter_by_car_reservation(filters.FilterSet):
    class Meta:
        model = CarReservation
        fields = ["car_service"]

    def filter_by_car_reservation(self, queryset, name, value):
        return True


class FilterReservation(filters.FilterSet):
    # Car Service
    model_id = filters.NumberFilter(
        field_name="car_reservations__car_service__model__id"
    )
    make_id = filters.NumberFilter(
        field_name="car_reservations__car_service__make__id"
    )
    car_subscription_type = filters.ChoiceFilter(
        field_name="car_reservations__subscription_option__type",
        choices=[('RIDE', 'Ride'), ('TRAVEL', 'Travel'), ('AIRPORT', 'Airport')]
    )
    car_subscription_duration = filters.NumberFilter(
        field_name="car_reservations__subscription_option__duration_hours"
    )
    
    # Hotel Service
    number_of_rooms = filters.NumberFilter(
        field_name='hotel_reservations__hotel_service__number_of_rooms'
    )
    number_of_beds = filters.NumberFilter(
        field_name='hotel_reservations__hotel_service__number_of_beds'
    )
    features = filters.ModelMultipleChoiceFilter(
        field_name='hotel_reservations__hotel_service__features',
        queryset=HotelServiceFeature.objects.all(),
        to_field_name='id'
    )

    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Reservation
        fields = ["status", "user", "created_by", "payment_method"]
