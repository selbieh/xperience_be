from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drfpasswordless.serializers import CallbackTokenAuthSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "mobile", "wallet", "is_staff", "points"]
        read_only_fields = ["wallet"]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and request.user and not request.user.is_staff:
            fields['is_staff'].read_only = True
        return fields

class CustomCallbackTokenAuthSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField()
    class Meta:
        model = User
        fields = ['id', 'mobile']

