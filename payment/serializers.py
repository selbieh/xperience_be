from rest_framework import serializers
from payment.models import Transaction
from payment.gateways import PayTabsGateway
from django.db import transaction as t
from payment.gateways.hmac_validation import hmac_validate
import logging
from users.serializers import UserProfileSerializer
from reservations.models import Reservation


from rest_framework import serializers
from .models import Transaction, Reservation

class PaySerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()

    def validate_reservation_id(self, value):
        try:
            reservation = Reservation.objects.get(id=value)
        except Reservation.DoesNotExist:
            raise serializers.ValidationError("Invalid reservation ID")
        return value

    def create_transaction(self, reservation, total_amount):
        user = reservation.user
        transaction = Transaction.objects.create(
            user=user,
            reservation=reservation,
            amount=total_amount,
            pending=True
        )
        return transaction

    def save(self, **kwargs):
        reservation_id = self.validated_data['reservation_id']
        reservation = Reservation.objects.get(id=reservation_id)
        
        # Calculate total amount
        car_reservations = reservation.car_reservations.all()
        hotel_reservations = reservation.hotel_reservations.all()
        total_amount = sum([cr.final_price for cr in car_reservations if cr.final_price]) + \
                       sum([hr.final_price for hr in hotel_reservations if hr.final_price])

        if total_amount <= 0:
            raise serializers.ValidationError("Total amount must be greater than zero")

        transaction = self.create_transaction(reservation, total_amount)  # Create transaction with total_amount

        # Process payment via PayTabs
        gateway = PayTabsGateway()
        _status, response = gateway.process_payment(user=reservation.user, price=float(total_amount), cart_id=transaction.id)
        if not _status:
            transaction.pending = False
            transaction.save()
            raise serializers.ValidationError("Payment initiation failed")

        json_response = response.json()
        transaction.tran_ref = json_response.get("tran_ref")
        transaction.save(update_fields=["tran_ref", "amount"])

        return {
            'redirect_url': json_response.get('redirect_url')
        }



class PaymentResultSerializer(serializers.Serializer):
    response_status = serializers.CharField()
    response_code = serializers.CharField()
    response_message = serializers.CharField()
    acquirer_ref = serializers.CharField()


class CallBackSerializer(serializers.Serializer):
    tran_ref = serializers.CharField()
    cart_id = serializers.CharField()
    tran_total = serializers.CharField()
    payment_result = PaymentResultSerializer()

    def validate(self, data):
        request = self.context["request"]
        transaction = Transaction.objects.filter(tran_ref=data["tran_ref"], id=data["cart_id"], success=False)
        if not transaction.exists():
            raise serializers.ValidationError("invalid transaction")
        signature = request.headers.get("signature")
        if not hmac_validate(signature=signature, payload=request.data):
            raise serializers.ValidationError("Hmac Validation Failed.")
        self.transaction = transaction.last()

        return data

    def save(self):
        payment_result = self.validated_data["payment_result"]
        transaction = self.transaction
        transaction.data.update(self.validated_data)
        transaction.pending = False
        transaction.response_code = payment_result.get("response_code")
        transaction.response_message = payment_result.get("response_message")
        if payment_result.get("response_status") == "A":
            transaction.success = True
            transaction.reservation.update(payment_status="CONFIRMED")
            transaction_ids = [transaction.id for transaction in transaction.reservation.all()]
        transaction.save()
        return transaction


class TransactionSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ["user", "reservation", "amount", "tran_ref", "success", "pending", "refunded", "status"]

    def get_status(self, obj):
        if obj.success and not obj.refunded:
            return "success"
        if obj.pending:
            return "pending"
        if not obj.success and not obj.pending:
            return "failed"
        if obj.refunded:
            return "refunded"
        return ""
