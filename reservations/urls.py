from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet, FilterReservationViewSet

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename="reservations")
router.register(r'filter-reservations', FilterReservationViewSet, basename='filter_reservations')

urlpatterns = [
    path('', include(router.urls)),
]
