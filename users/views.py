from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserProfileSerializer, CustomCallbackTokenAuthSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from drfpasswordless.serializers import CallbackTokenAuthSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class UserProfileViewSet(ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['mobile']
    filterset_fields = ['is_staff']


    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):

        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    def destroy(self, request, *args, **kwargs):
        # Custom response for delete action
        return Response({"message": "Your account has been deleted."}, status=status.HTTP_200_OK)


class CustomObtainAuthToken(APIView):
    permission_classes = [AllowAny]
    serializer_class = CallbackTokenAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            user_data = UserProfileSerializer(user).data
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CustomObtainAuthToken(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = CustomCallbackTokenAuthSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid(raise_exception=True):
#             mobile = serializer.validated_data['mobile']
#             user = User.objects.get(mobile=mobile)
#             refresh = RefreshToken.for_user(user)
#             user_data = UserProfileSerializer(user).data
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user': user_data
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
