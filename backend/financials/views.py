import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption
from .serializers import DepositProductSerializer, SavingProductSerializer

@api_view(['GET'])
def save_financial_products(request):
    """
    금융감독원 API로부터 예금 및 적금 상품 목록을 받아와 DB에 저장합니다.
    """
    api_key = settings.FSS_API_KEY
    # 예금 상품 목록
    deposit_url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    # 적금 상품 목록
    saving_url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'

    # 예금 데이터 저장
    try:
        deposit_response = requests.get(deposit_url).json()
        for product_data in deposit_response['result']['baseList']:
            deposit_product, created = DepositProduct.objects.update_or_create(
                fin_prdt_cd=product_data['fin_prdt_cd'],
                defaults={
                    'kor_co_nm': product_data['kor_co_nm'],
                    'fin_prdt_nm': product_data['fin_prdt_nm'],
                    'etc_note': product_data['etc_note'],
                    'join_deny': int(product_data.get('join_deny', 0) or 0),
                    'join_member': product_data['join_member'],
                    'join_way': product_data['join_way'],
                    'spcl_cnd': product_data['spcl_cnd'],
                }
            )
            for option_data in deposit_response['result']['optionList']:
                if option_data['fin_prdt_cd'] == product_data['fin_prdt_cd']:
                    DepositOption.objects.update_or_create(
                        deposit_product=deposit_product,
                        intr_rate_type=option_data['intr_rate_type'],
                        save_trm=option_data['save_trm'],
                        defaults={
                            'intr_rate_type_nm': option_data['intr_rate_type_nm'],
                            'intr_rate': option_data.get('intr_rate') or -1,
                            'intr_rate2': option_data.get('intr_rate2') or -1,
                        }
                    )
    except requests.exceptions.RequestException as e:
        return Response({'error': f"예금 API 요청 오류: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 적금 데이터 저장
    try:
        saving_response = requests.get(saving_url).json()
        for product_data in saving_response['result']['baseList']:
            saving_product, created = SavingProduct.objects.update_or_create(
                fin_prdt_cd=product_data['fin_prdt_cd'],
                defaults={
                    'kor_co_nm': product_data['kor_co_nm'],
                    'fin_prdt_nm': product_data['fin_prdt_nm'],
                    'etc_note': product_data['etc_note'],
                    'join_deny': int(product_data.get('join_deny', 0) or 0),
                    'join_member': product_data['join_member'],
                    'join_way': product_data['join_way'],
                    'spcl_cnd': product_data['spcl_cnd'],
                }
            )
            for option_data in saving_response['result']['optionList']:
                if option_data['fin_prdt_cd'] == product_data['fin_prdt_cd']:
                    SavingOption.objects.update_or_create(
                        saving_product=saving_product,
                        intr_rate_type=option_data['intr_rate_type'],
                        rsrv_type=option_data['rsrv_type'],
                        save_trm=option_data['save_trm'],
                        defaults={
                            'intr_rate_type_nm': option_data['intr_rate_type_nm'],
                            'rsrv_type_nm': option_data['rsrv_type_nm'],
                            'intr_rate': option_data.get('intr_rate') or -1,
                            'intr_rate2': option_data.get('intr_rate2') or -1,
                        }
                    )
    except requests.exceptions.RequestException as e:
        return Response({'error': f"적금 API 요청 오류: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "금융 상품 정보가 성공적으로 저장되었습니다."}, status=status.HTTP_200_OK)


@api_view(['GET'])
def deposit_products(request):
    products = DepositProduct.objects.all()
    serializer = DepositProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def deposit_product_detail(request, pk):
    try:
        product = DepositProduct.objects.get(pk=pk)
        serializer = DepositProductSerializer(product)
        return Response(serializer.data)
    except DepositProduct.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def saving_products(request):
    products = SavingProduct.objects.all()
    serializer = SavingProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def saving_product_detail(request, pk):
    try:
        product = SavingProduct.objects.get(pk=pk)
        serializer = SavingProductSerializer(product)
        return Response(serializer.data)
    except SavingProduct.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)