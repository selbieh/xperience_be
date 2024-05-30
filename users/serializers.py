from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drfpasswordless.serializers import CallbackTokenAuthSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id", "first_name", "last_name", "mobile", "wallet"]

class CustomCallbackTokenAuthSerializer(CallbackTokenAuthSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = validated_data['user']

        refresh = RefreshToken.for_user(user)
        validated_data['refresh'] = str(refresh)
        validated_data['access'] = str(refresh.access_token)

        return validated_data