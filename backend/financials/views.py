# backend/financials/views.py

import datetime
import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption, UserDeposit, UserSaving
from .serializers import DepositProductSerializer, SavingProductSerializer, UserDepositSerializer, UserSavingSerializer

# ... (save_financial_products, deposit_products, deposit_product_detail, saving_products, saving_product_detail 함수는 동일) ...

@api_view(['GET'])
def save_financial_products(request):
    """
    금융감독원 API로부터 예금 및 적금 상품 목록을 받아와 DB에 저장합니다.
    """
    api_key = settings.FSS_API_KEY
    
    today = datetime.date.today()
    dcls_months = []
    for i in range(12):
        year = today.year
        month = today.month - i
        while month <= 0:
            month += 12
            year -= 1
        dcls_months.append(f"{year}{str(month).zfill(2)}")
    
    dcls_months = sorted(list(set(dcls_months)), reverse=True)

    # 예금 데이터 저장
    for dcls_month in dcls_months:
        deposit_url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1&dcls_month={dcls_month}'
        try:
            deposit_response = requests.get(deposit_url).json()
            if deposit_response.get('result'):
                DepositProduct.objects.filter(dcls_month=dcls_month).delete()

                for product_data in deposit_response['result']['baseList']:
                    deposit_product = DepositProduct.objects.create(
                        fin_prdt_cd=product_data['fin_prdt_cd'],
                        kor_co_nm=product_data['kor_co_nm'],
                        fin_prdt_nm=product_data['fin_prdt_nm'],
                        etc_note=product_data['etc_note'],
                        join_deny=int(product_data.get('join_deny', 0) or 0),
                        join_member=product_data['join_member'],
                        join_way=product_data['join_way'],
                        spcl_cnd=product_data['spcl_cnd'],
                        dcls_month=product_data.get('dcls_month'),
                        fin_co_no=product_data.get('fin_co_no'),
                        mtrt_int=product_data.get('mtrt_int'),
                        max_limit=product_data.get('max_limit'),
                    )
                for option_data in deposit_response['result']['optionList']:
                    try:
                        product = DepositProduct.objects.get(
                            fin_prdt_cd=option_data['fin_prdt_cd'],
                            fin_co_no=option_data['fin_co_no']
                        )
                        DepositOption.objects.create(
                            deposit_product=product,
                            intr_rate_type=option_data['intr_rate_type'],
                            save_trm=option_data['save_trm'],
                            intr_rate_type_nm=option_data['intr_rate_type_nm'],
                            intr_rate=option_data.get('intr_rate') or -1,
                            intr_rate2=option_data.get('intr_rate2') or -1,
                        )
                    except DepositProduct.DoesNotExist:
                        print(f"Warning: DepositProduct for option {option_data['fin_prdt_cd']} not found. Skipping option.")
        except requests.exceptions.RequestException as e:
            print(f"예금 API 요청 오류 (월: {dcls_month}): {e}")
        except Exception as e:
            print(f"예금 데이터 처리 중 오류 발생 (월: {dcls_month}): {e}")

    # 적금 데이터 저장
    for dcls_month in dcls_months:
        saving_url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1&dcls_month={dcls_month}'
        try:
            saving_response = requests.get(saving_url).json()
            if saving_response.get('result'):
                SavingProduct.objects.filter(dcls_month=dcls_month).delete()

                for product_data in saving_response['result']['baseList']:
                    saving_product = SavingProduct.objects.create(
                        fin_prdt_cd=product_data['fin_prdt_cd'],
                        kor_co_nm=product_data['kor_co_nm'],
                        fin_prdt_nm=product_data['fin_prdt_nm'],
                        etc_note=product_data['etc_note'],
                        join_deny=int(product_data.get('join_deny', 0) or 0),
                        join_member=product_data['join_member'],
                        join_way=product_data['join_way'],
                        spcl_cnd=product_data['spcl_cnd'],
                        dcls_month=product_data.get('dcls_month'),
                        fin_co_no=product_data.get('fin_co_no'),
                        mtrt_int=product_data.get('mtrt_int'),
                        max_limit=product_data.get('max_limit'),
                    )
                for option_data in saving_response['result']['optionList']:
                    try:
                        product = SavingProduct.objects.get(
                            fin_prdt_cd=option_data['fin_prdt_cd'],
                            fin_co_no=option_data['fin_co_no']
                        )
                        SavingOption.objects.create(
                            saving_product=product,
                            intr_rate_type=option_data['intr_rate_type'],
                            rsrv_type=option_data['rsrv_type'],
                            save_trm=option_data['save_trm'],
                            intr_rate_type_nm=option_data['intr_rate_type_nm'],
                            rsrv_type_nm=option_data['rsrv_type_nm'],
                            intr_rate=option_data.get('intr_rate') or -1,
                            intr_rate2=option_data.get('intr_rate2') or -1,
                        )
                    except SavingProduct.DoesNotExist:
                        print(f"Warning: SavingProduct for option {option_data['fin_prdt_cd']} not found. Skipping option.")
        except requests.exceptions.RequestException as e:
            print(f"적금 API 요청 오류 (월: {dcls_month}): {e}")
        except Exception as e:
            print(f"적금 데이터 처리 중 오류 발생 (월: {dcls_month}): {e}")

    return Response({"message": "금융 상품 정보가 성공적으로 저장되었습니다."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def deposit_products(request):
    kor_co_nm = request.query_params.get('kor_co_nm')
    dcls_month = request.query_params.get('dcls_month')

    flat_products = []
    products = DepositProduct.objects.all().prefetch_related('options') 
    
    if kor_co_nm:
        products = products.filter(kor_co_nm__icontains=kor_co_nm)
    if dcls_month:
        products = products.filter(dcls_month=dcls_month)

    for product in products:
        sorted_options = sorted(product.options.all(), key=lambda x: x.save_trm)
        for option in sorted_options:
            flat_products.append({
                'id': product.id, 
                'dcls_month': product.dcls_month,
                'kor_co_nm': product.kor_co_nm,
                'fin_prdt_nm': product.fin_prdt_nm,
                'save_trm': option.save_trm, 
                'intr_rate': option.intr_rate,
                'intr_rate2': option.intr_rate2,
                'intr_rate_type_nm': option.intr_rate_type_nm,
            })
    
    return Response(flat_products)

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
    kor_co_nm = request.query_params.get('kor_co_nm')
    dcls_month = request.query_params.get('dcls_month')

    flat_products = []
    products = SavingProduct.objects.all().prefetch_related('options')

    if kor_co_nm:
        products = products.filter(kor_co_nm__icontains=kor_co_nm)
    if dcls_month:
        products = products.filter(dcls_month=dcls_month)

    for product in products:
        sorted_options = sorted(product.options.all(), key=lambda x: x.save_trm)
        for option in sorted_options:
            flat_products.append({
                'id': product.id, 
                'dcls_month': product.dcls_month,
                'kor_co_nm': product.kor_co_nm,
                'fin_prdt_nm': product.fin_prdt_nm,
                'save_trm': option.save_trm, 
                'intr_rate': option.intr_rate,
                'intr_rate2': option.intr_rate2,
                'intr_rate_type_nm': option.intr_rate_type_nm,
                'rsrv_type_nm': option.rsrv_type_nm, 
            })
    
    return Response(flat_products)

@api_view(['GET'])
def saving_product_detail(request, pk):
    try:
        product = SavingProduct.objects.get(pk=pk)
        serializer = SavingProductSerializer(product)
        return Response(serializer.data)
    except SavingProduct.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_deposit_product(request, pk):  # product_pk를 pk로 변경
    product = get_object_or_404(DepositProduct, pk=pk) # 여기도 pk로 변경
    serializer = UserDepositSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, deposit_product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_saving_product(request, pk):  # product_pk를 pk로 변경
    product = get_object_or_404(SavingProduct, pk=pk) # 여기도 pk로 변경
    serializer = UserSavingSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, saving_product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_deposit_subscription(request, pk):
    """
    사용자가 가입한 예금 상품을 삭제(가입 취소)합니다.
    """
    subscription = get_object_or_404(UserDeposit, pk=pk)
    if request.user != subscription.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    subscription.delete()
    return Response(data={'message': f'예금 가입 정보({pk})가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_saving_subscription(request, pk):
    """
    사용자가 가입한 적금 상품을 삭제(가입 취소)합니다.
    """
    subscription = get_object_or_404(UserSaving, pk=pk)
    if request.user != subscription.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    subscription.delete()
    return Response(data={'message': f'적금 가입 정보({pk})가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)