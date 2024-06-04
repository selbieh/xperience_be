from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from drfpasswordless.serializers import CallbackTokenAuthSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserProfileViewSet(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    def get_object(self):
        return self.request.user



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
