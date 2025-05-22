# backend/recommendations/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import FinancialProduct, ProductOption
from products.serializers import FinancialProductListSerializer # 상품 목록 시리얼라이저 재활용
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_basic_recommendations(request):
    user = request.user

    # 사용자 정보 (나이, 연봉, 자산) 가져오기 [cite: 95]
    age = user.age
    annual_salary = user.annual_salary
    current_assets = user.current_assets

    # 매우 단순한 추천 로직 (예시) [cite: 88]
    # 실제로는 더 정교한 로직, DB 쿼리, 또는 ML 모델 사용 필요 [cite: 97]
    recommended_products = []

    # 예시: 30세 미만이고 연봉이 5000만원 이상인 경우 특정 유형의 고금리 단기 적금 추천
    if age and age < 30 and annual_salary and annual_salary >= 50000000:
        # 예시로, 금리가 높은 상위 2개 적금 상품을 추천 (옵션 중 최고 우대 금리 기준)
        # 실제 구현 시에는 ProductOption의 intr_rate2 등을 고려하여 정렬 및 필터링
        savings = FinancialProduct.objects.filter(product_type='saving') \
                        .annotate(max_rate=models.Max('options__intr_rate2')) \
                        .order_by('-max_rate')[:2] # 최고 금리 기준 상위 2개
        recommended_products.extend(savings)
    
    # 예시: 자산이 1억 이상인 경우 안정적인 예금 상품 추천
    elif current_assets and current_assets >= 100000000:
        deposits = FinancialProduct.objects.filter(product_type='deposit') \
                        .annotate(max_rate=models.Max('options__intr_rate2')) \
                        .order_by('-max_rate')[:2]
        recommended_products.extend(deposits)
    
    # 기본 추천: 모든 상품 중 인기 상품 (여기서는 단순히 최신 상품 2개)
    if not recommended_products:
        recommended_products = FinancialProduct.objects.all().order_by('-id')[:2] # 단순 예시

    # 중복 제거 (혹시나 로직상 중복이 발생할 수 있다면)
    final_recommendations = list(set(recommended_products))
    
    serializer = FinancialProductListSerializer(final_recommendations, many=True)
    return Response(serializer.data)