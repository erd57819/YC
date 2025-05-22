# backend/accounts/serializers.py
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.db import transaction
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)
    # 회원가입 시 연봉, 자산도 받도록 하려면 아래 주석 해제 및 required 설정
    # annual_salary = serializers.IntegerField(required=False, allow_null=True) 
    # current_assets = serializers.IntegerField(required=False, allow_null=True)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.age = self.validated_data.get('age', None)
        # user.annual_salary = self.validated_data.get('annual_salary', None) # 주석 해제 시
        # user.current_assets = self.validated_data.get('current_assets', None) # 주석 해제 시
        user.save()
        return user

class CustomUserDetailsSerializer(UserDetailsSerializer):
    subscribed_products_display = serializers.SerializerMethodField()
    # 추가된 필드
    annual_salary = serializers.IntegerField(required=False, allow_null=True)
    current_assets = serializers.IntegerField(required=False, allow_null=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'age', 'subscribed_products', 'subscribed_products_display',
            'annual_salary', 'current_assets' # 추가
        )
        read_only_fields = UserDetailsSerializer.Meta.read_only_fields + ('subscribed_products_display', 'username')

    def get_subscribed_products_display(self, instance):
        if instance.subscribed_products:
            return [prod_id.strip() for prod_id in instance.subscribed_products.split(',') if prod_id.strip()]
        return []

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.age = validated_data.get('age', instance.age)
        instance.subscribed_products = validated_data.get('subscribed_products', instance.subscribed_products)
        instance.annual_salary = validated_data.get('annual_salary', instance.annual_salary) # 추가
        instance.current_assets = validated_data.get('current_assets', instance.current_assets) # 추가
        
        instance = super().update(instance, validated_data)
        # instance.save() # super().update() 에서 호출됨
        return instance