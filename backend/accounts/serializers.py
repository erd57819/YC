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
    annual_salary = serializers.IntegerField(required=False, allow_null=True)
    current_assets = serializers.IntegerField(required=False, allow_null=True)
    
    # [추가] 가입한 상품들의 상세 정보를 위한 필드
    subscribed_products_details = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'age', 
            'subscribed_products',          # 사용자가 직접 수정할 수 있는 상품 ID 문자열
            'subscribed_products_display',  # 단순히 ID 목록을 보여주는 필드 (읽기 전용)
            'annual_salary', 
            'current_assets',
            'subscribed_products_details'   # [추가] 가입 상품 상세 정보 (읽기 전용, 차트용)
        )
        read_only_fields = UserDetailsSerializer.Meta.read_only_fields + (
            'subscribed_products_display', 
            'username',
            'subscribed_products_details'   # [추가] 읽기 전용 필드에 포함
        )

    def get_subscribed_products_display(self, instance):
        if instance.subscribed_products:
            return [prod_id.strip() for prod_id in instance.subscribed_products.split(',') if prod_id.strip()]
        return []

    # [추가] 가입한 상품들의 상세 정보를 가져오는 메소드
    def get_subscribed_products_details(self, instance):
        if not instance.subscribed_products:
            return []
        
        product_codes = [code.strip() for code in instance.subscribed_products.split(',') if code.strip()]
        
        products = []
        for code in product_codes:
            try:
                # 상품 코드로 FinancialProduct 객체를 가져옵니다.
                # 이 때, options 정보도 함께 가져오기 위해 prefetch_related 등을 고려할 수 있으나,
                # FinancialProductSerializer가 이미 options를 처리하고 있다면 그대로 사용 가능합니다.
                product = FinancialProduct.objects.get(fin_prdt_cd=code)
                products.append(product)
            except FinancialProduct.DoesNotExist:
                # 해당 코드를 가진 상품이 DB에 없으면 무시하고 계속 진행
                continue
        
        # FinancialProductSerializer를 사용하여 상품 목록(옵션 포함)을 직렬화합니다.
        return FinancialProductSerializer(products, many=True, context=self.context).data

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.age = validated_data.get('age', instance.age)
        # subscribed_products 필드는 사용자가 직접 쉼표로 구분된 문자열로 수정할 수 있도록 합니다.
        instance.subscribed_products = validated_data.get('subscribed_products', instance.subscribed_products)
        instance.annual_salary = validated_data.get('annual_salary', instance.annual_salary)
        instance.current_assets = validated_data.get('current_assets', instance.current_assets)
        
        # first_name, last_name 등 UserDetailsSerializer의 기본 필드들도 업데이트 되도록 super() 호출
        instance = super().update(instance, validated_data)
        # instance.save() # super().update() 내부에서 instance.save()가 호출되므로 중복입니다.
        return instance