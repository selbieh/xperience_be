from rest_framework import serializers
from .models import Policy, FAQ, UserNotification

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['key', 'content']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ['id', 'title', 'body', 'created_at', 'read']
        read_only_fields= ['id', 'title', 'body', 'created_at']