from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drfpasswordless.serializers import CallbackTokenAuthSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "mobile", "wallet", "is_staff"]
        read_only_fields = ["wallet"]

class CustomCallbackTokenAuthSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField()
    class Meta:
        model = User
        fields = ['id', 'mobile']

