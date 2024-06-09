from rest_framework.viewsets import ModelViewSet
from .models import Policy, FAQ
from .serializers import PolicySerializer, FAQSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

class PolicyViewSet(ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    filterset_fields = ['key']
    pagination_class = None

    def get_permissions(self):
        if self.request.method in ['GET']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    

class FAQViewSet(ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
