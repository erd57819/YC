# accounts/serializers.py

from rest_framework import serializers # <--- 이 줄을 추가하세요.
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.db import transaction
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    # 이제 'serializers.IntegerField'가 정상적으로 동작합니다.
    age = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.age = self.validated_data.get('age', None)
        user.save()
        return user

# 사용자 상세 정보 시리얼라이저
class CustomUserDetailsSerializer(UserDetailsSerializer):
    # 이제 'serializers.SerializerMethodField'가 정상적으로 동작합니다.
    subscribed_products_display = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('age', 'subscribed_products', 'subscribed_products_display')
        read_only_fields = UserDetailsSerializer.Meta.read_only_fields + ('subscribed_products_display', 'username') # 이전 답변에서 username을 read_only로 추가했었습니다.

    def get_subscribed_products_display(self, instance):
        if instance.subscribed_products:
            return [prod_id.strip() for prod_id in instance.subscribed_products.split(',') if prod_id.strip()]
        return []

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.age = validated_data.get('age', instance.age)
        instance.subscribed_products = validated_data.get('subscribed_products', instance.subscribed_products)
        
        instance = super().update(instance, validated_data)
        instance.save()
        return instance