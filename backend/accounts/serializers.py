# accounts/serializers.py

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer # 추가
from rest_framework import serializers
from django.db import transaction
from .models import User # 추가 (이미 있다면 생략)

class CustomRegisterSerializer(RegisterSerializer):
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
    # Meta 클래스에 subscribed_products, age 추가
    # 기존 UserDetailsSerializer는 username, email, first_name, last_name 등을 포함하고 있음
    subscribed_products_display = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('age', 'subscribed_products', 'subscribed_products_display')
        read_only_fields = UserDetailsSerializer.Meta.read_only_fields + ('subscribed_products_display',) # subscribed_products는 수정 가능하게

    def get_subscribed_products_display(self, instance):
        # subscribed_products 필드를 파싱하여 상품 객체 목록이나 이름 목록 등으로 변환하여 보여줄 수 있음
        # 여기서는 간단히 쉼표로 구분된 문자열을 리스트로 변환하여 반환
        if instance.subscribed_products:
            return [prod_id.strip() for prod_id in instance.subscribed_products.split(',') if prod_id.strip()]
        return []

    @transaction.atomic
    def update(self, instance, validated_data):
        # email, age, subscribed_products 등의 필드를 업데이트
        instance.age = validated_data.get('age', instance.age)
        # subscribed_products는 문자열 형태로 직접 받아서 저장하거나,
        # 또는 별도의 로직으로 처리 (예: 리스트를 받아서 쉼표 구분 문자열로 변환)
        instance.subscribed_products = validated_data.get('subscribed_products', instance.subscribed_products)
        
        # email은 UserDetailsSerializer의 update에서 처리되도록 할 수 있음
        # 또는 여기서 명시적으로 instance.email = validated_data.get('email', instance.email)
        
        # dj_rest_auth의 UserDetailsSerializer의 update 로직을 호출하여
        # username, first_name, last_name, email 등의 기본 필드도 업데이트되도록 함
        instance = super().update(instance, validated_data)
        instance.save()
        return instance