from rest_framework import serializers
from payment.models import Transaction
from payment.gateways import PayTabsGateway
from django.db import transaction as t
from payment.gateways.hmac_validation import hmac_validate
import logging
from users.serializers import CustomUserDetailsSerializer
from django.utils import timezone
from datetime import timedelta
from reservations.models import Reservation


class PaySerializer(serializers.Serializer):
    reservation = serializers.IntegerField()

    def validate_reservation(self, value):
        reservation = Reservation.objects.filter(id=value, status="pending")
        if not reservation.exists():
            raise serializers.ValidationError("no pending trnx")
        return reservation

    def save(self):
        with t.atomic():
            user = self.context.get("request").user
            tickets = self.validated_data["tickets"]
            transaction = Transaction.objects.create(user=user, organizer=tickets.last().event.organizer)
            price = 0
            fee = 0
            vat = 0
            for ticket in tickets:
                price += ticket.price
                fee += ticket.fee
                vat += ticket.vat
                transaction.tickets.add(ticket)
            transaction.save()
        gateway = PayTabsGateway()
        _status, response = gateway.process_payment(user=user, price=float(price), cart_id=transaction.id)
        if not _status:
            return False, response
        json_response = response.json()
        transaction.tran_ref = json_response.get("tran_ref")
        transaction.amount = price
        transaction.vat = vat
        transaction.fee = fee
        transaction.save(update_fields=["tran_ref", "amount", "vat", "fee"])

        return _status, {"redirect_url": json_response.get("redirect_url")}


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
            transaction.tickets.update(payment_status="paid")
            transaction_ids = [transaction.id for transaction in transaction.tickets.all()]
        transaction.save()
        return transaction


class TransactionSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ["user", "tickets", "amount", "tran_ref", "success", "pending", "refunded", "status"]

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
