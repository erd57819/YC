from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny # AllowAny는 테스트용, 실제로는 IsAuthenticated 권장
from django.shortcuts import get_object_or_404
from .models import FinancialProduct, ProductOption
from .serializers import FinancialProductSerializer, FinancialProductListSerializer
from django.contrib.auth import get_user_model # User 모델 가져오기
from django.db.models import Q # Q 객체 import

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny]) # 실제 서비스에서는 IsAuthenticated 또는 적절한 권한 설정
def product_list(request):
    """
    전체 금융 상품 목록 (예금 및 적금) 또는 특정 은행의 상품 목록을 반환합니다.
    Query Parameters:
        - type: 'deposit' 또는 'saving' (상품 타입 필터링)
        - bank: 은행 이름 (금융 회사명 필터링, 예: '우리은행')
    """
    products = FinancialProduct.objects.all().order_by('kor_co_nm', 'fin_prdt_nm')
    
    product_type = request.query_params.get('type')
    bank_name = request.query_params.get('bank')

    if product_type:
        products = products.filter(product_type=product_type)
    
    if bank_name:
        products = products.filter(kor_co_nm__icontains=bank_name) # 대소문자 구분 없이 포함 검색

    serializer = FinancialProductListSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny]) # 실제 서비스에서는 IsAuthenticated 또는 적절한 권한 설정
def product_detail(request, product_pk_or_code):
    """
    특정 금융 상품의 상세 정보를 반환합니다.
    product_pk_or_code: 상품의 PK(id) 또는 fin_prdt_cd
    """
    try:
        # 먼저 pk (id)로 조회 시도
        product = FinancialProduct.objects.get(pk=int(product_pk_or_code))
    except (ValueError, FinancialProduct.DoesNotExist):
        # pk가 아니거나 해당 pk가 없으면 fin_prdt_cd로 조회 시도
        try:
            product = FinancialProduct.objects.get(fin_prdt_cd=str(product_pk_or_code))
        except FinancialProduct.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            
    serializer = FinancialProductSerializer(product)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 상품 가입은 로그인한 사용자만 가능
def subscribe_product(request, product_pk_or_code):
    """
    사용자가 특정 금융 상품에 가입합니다.
    사용자의 subscribed_products 필드에 해당 상품의 fin_prdt_cd를 추가합니다.
    """
    try:
        product = FinancialProduct.objects.get(pk=int(product_pk_or_code))
    except (ValueError, FinancialProduct.DoesNotExist):
        try:
            product = FinancialProduct.objects.get(fin_prdt_cd=str(product_pk_or_code))
        except FinancialProduct.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    product_code_to_add = product.fin_prdt_cd

    # 사용자의 subscribed_products 필드 가져오기 (쉼표로 구분된 문자열)
    subscribed_list_str = user.subscribed_products
    
    if subscribed_list_str:
        subscribed_codes = [code.strip() for code in subscribed_list_str.split(',') if code.strip()]
        if product_code_to_add not in subscribed_codes:
            subscribed_codes.append(product_code_to_add)
            user.subscribed_products = ','.join(subscribed_codes)
        else:
            # 이미 가입된 상품인 경우, 여기서는 별도 처리 없이 성공으로 간주하거나,
            # 이미 가입했다는 메시지를 반환할 수 있습니다.
            return Response({'message': '이미 가입한 상품입니다.', 'subscribed_products': subscribed_codes}, status=status.HTTP_200_OK)
    else:
        user.subscribed_products = product_code_to_add
        subscribed_codes = [product_code_to_add]
        
    user.save()
    
    # CustomUserDetailsSerializer를 사용하여 업데이트된 사용자 정보 반환 (선택 사항)
    # from accounts.serializers import CustomUserDetailsSerializer
    # user_serializer = CustomUserDetailsSerializer(user)
    # return Response({'message': '상품에 성공적으로 가입했습니다.', 'user': user_serializer.data}, status=status.HTTP_200_OK)
    return Response({'message': '상품에 성공적으로 가입했습니다.', 'subscribed_product_code': product_code_to_add, 'subscribed_products': subscribed_codes}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unsubscribe_product(request, product_pk_or_code):
    """
    사용자가 특정 금융 상품 가입을 해지합니다.
    사용자의 subscribed_products 필드에서 해당 상품의 fin_prdt_cd를 제거합니다.
    """
    try:
        product = FinancialProduct.objects.get(pk=int(product_pk_or_code))
    except (ValueError, FinancialProduct.DoesNotExist):
        try:
            product = FinancialProduct.objects.get(fin_prdt_cd=str(product_pk_or_code))
        except FinancialProduct.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    product_code_to_remove = product.fin_prdt_cd

    subscribed_list_str = user.subscribed_products
    
    if subscribed_list_str:
        subscribed_codes = [code.strip() for code in subscribed_list_str.split(',') if code.strip()]
        if product_code_to_remove in subscribed_codes:
            subscribed_codes.remove(product_code_to_remove)
            user.subscribed_products = ','.join(subscribed_codes) if subscribed_codes else None # 리스트가 비면 None (또는 빈 문자열)
            user.save()
            return Response({'message': '상품 가입을 성공적으로 해지했습니다.', 'unsubscribed_product_code': product_code_to_remove, 'subscribed_products': subscribed_codes}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '해당 상품에 가입되어 있지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': '가입한 상품이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)