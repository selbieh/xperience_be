from rest_framework import serializers
from .models import Policy, FAQ, UserNotification, AdminNotification

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

class AdminNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminNotification
        fields = ['id', 'title', 'body', 'created_at', 'read', 'user', 'reservation']
        read_only_fields= ['id', 'title', 'body', 'created_at', 'user', 'reservation']