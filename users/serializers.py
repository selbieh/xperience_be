from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id", "first_name", "last_name", "mobile", "wallet"]
    