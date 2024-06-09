from rest_framework import serializers
from .models import Policy, FAQ

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['key', 'content']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']
