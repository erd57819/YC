from rest_framework import serializers
from .models import Gold, Silver

class GoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gold
        fields = '__all__'

class SilverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Silver
        fields = '__all__'