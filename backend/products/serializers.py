from rest_framework import serializers
from .models import FinancialProduct, ProductOption

class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        # product 필드는 제외하거나, Product ID만 표시하도록 할 수 있음
        # fields = '__all__' 
        exclude = ('product', 'fin_prdt_cd') # 부모 정보 중복 회피
        # depth = 1 # product 객체 전체를 보여주고 싶을 때 (하지만 중복 정보 가능성)

class FinancialProductSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True, read_only=True) # 상품에 연결된 옵션들을 함께 보여줌
    # product_type_display = serializers.CharField(source='get_product_type_display', read_only=True) # choices 필드의 표시 이름

    class Meta:
        model = FinancialProduct
        fields = '__all__'
        # depth = 1 # 옵션까지 한 번에 보여주려면 필요할 수 있지만, options 필드가 이미 처리 중

class FinancialProductListSerializer(serializers.ModelSerializer):
    # 목록 조회 시에는 모든 옵션을 다 보여줄 필요가 없을 수 있음
    # 필요하다면 옵션 중 대표적인 정보만 요약해서 보여주는 필드를 추가
    # 예: 최저/최고 금리, 최단/최장 기간 등
    class Meta:
        model = FinancialProduct
        fields = ('id', 'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'product_type', 'etc_note', 'join_way', 'spcl_cnd')
        # 필요한 필드만 선택하여 가볍게 구성