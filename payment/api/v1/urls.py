from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"payment", views.PaymentViewSet, basename="payment")
router.register(r"transaction", views.TransactionViewSet, basename="transaction")


urlpatterns = [
    path("", include(router.urls)),
]
