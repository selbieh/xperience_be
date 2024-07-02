from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import PaySerializer, CallBackSerializer, TransactionSerializer, RefundSerializer
from rest_framework.decorators import action
from rest_framework import viewsets, status
from payment.models import Transaction
from payment.filters import TransactionFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["POST"])
    def pay(self, request):
        seralizer = PaySerializer(data=request.data, context={"request": request})
        seralizer.is_valid(raise_exception=True)
        _status, resposne = seralizer.save()
        if not _status:
            return Response({"message": resposne}, status=status.HTTP_400_BAD_REQUEST)
        return Response(resposne)

    """
    Open Endpoint To accept the call-back from Gateway to approve/reject transaction
    """

    @action(detail=False, methods=["POST"], url_path="call-back", permission_classes=[])
    def call_back(self, request):
        data = request.data
        serializer = CallBackSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TransactionFilter
    search_fields = ["tran_ref", "user__name", "user__email", "user__mobile_number"]

    def get_queryset(self):
        qs = Transaction.objects.all()
        return qs
