# backend/accounts/serializers.py
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.db import transaction
from .models import User
from products.models import FinancialProduct # [추가] 가입 상품 상세 정보 조회를 위해 import
from products.serializers import FinancialProductSerializer # [추가] 상품 상세 정보를 직렬화하기 위해 import

class CustomRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)
    # 회원가입 시 연봉, 자산도 받도록 수정
    annual_salary = serializers.IntegerField(required=False, allow_null=True) 
    current_assets = serializers.IntegerField(required=False, allow_null=True)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.age = self.validated_data.get('age', None)
        user.annual_salary = self.validated_data.get('annual_salary', None) # 주석 해제 및 값 할당
        user.current_assets = self.validated_data.get('current_assets', None) # 주석 해제 및 값 할당
        user.save()
        return user

class CustomUserDetailsSerializer(UserDetailsSerializer):
    subscribed_products_display = serializers.SerializerMethodField()
    annual_salary = serializers.IntegerField(required=False, allow_null=True)
    current_assets = serializers.IntegerField(required=False, allow_null=True)
    
    subscribed_products_details = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'age', 
            'subscribed_products',
            'subscribed_products_display',
            'annual_salary', 
            'current_assets',
            'subscribed_products_details'
        )
        read_only_fields = UserDetailsSerializer.Meta.read_only_fields + (
            'subscribed_products_display', 
            'username',
            'subscribed_products_details'
        )

    def get_subscribed_products_display(self, instance):
        if instance.subscribed_products:
            return [prod_id.strip() for prod_id in instance.subscribed_products.split(',') if prod_id.strip()]
        return []

    def get_subscribed_products_details(self, instance):
        if not instance.subscribed_products:
            return []
        
        product_codes = [code.strip() for code in instance.subscribed_products.split(',') if code.strip()]
        
        # N+1 쿼리 방지를 위해 한 번에 모든 상품 조회
        products_queryset = FinancialProduct.objects.filter(fin_prdt_cd__in=product_codes)
        
        # API에서 받아온 product_codes 순서를 유지하기 위해 딕셔너리 사용
        products_dict = {product.fin_prdt_cd: product for product in products_queryset}
        
        # 원래 product_codes 순서대로 정렬된 상품 리스트 생성
        ordered_products = []
        for code in product_codes:
            if code in products_dict:
                ordered_products.append(products_dict[code])
        
        return FinancialProductSerializer(ordered_products, many=True, context=self.context).data

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.age = validated_data.get('age', instance.age)
        instance.subscribed_products = validated_data.get('subscribed_products', instance.subscribed_products)
        instance.annual_salary = validated_data.get('annual_salary', instance.annual_salary)
        instance.current_assets = validated_data.get('current_assets', instance.current_assets)
        
        instance = super().update(instance, validated_data)
        return instance