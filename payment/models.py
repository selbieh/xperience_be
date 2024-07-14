from django.db import models
from django_extensions.db.models import TimeStampedModel
from users.models import User
from reservations.models import Reservation


class Transaction(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    reservation = models.ForeignKey(Reservation, related_name="transactions", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tran_ref = models.CharField(max_length=255, null=True)
    response_code = models.CharField(max_length=255, null=True)
    response_message = models.CharField(max_length=255, null=True)
    success = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)
    refunded = models.BooleanField(default=False)
    data = models.JSONField(default=dict)
    is_refund = models.BooleanField(default=False)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wallet = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"transaction {self.id}"
