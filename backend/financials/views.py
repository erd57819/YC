# backend/financials/views.py
import datetime
import requests
import json
from django.conf import settings
from django.db.models import Max, Q, Exists, OuterRef
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption, UserDeposit, UserSaving
from accounts.models import User # User 모델 임포트
from .serializers import DepositProductSerializer, SavingProductSerializer, UserDepositSerializer, UserSavingSerializer
from openai import OpenAI

# --- 금융 상품 정보 저장 API (save_financial_products) ---
# (이전 답변의 save_financial_products 함수와 동일하게 유지)
@api_view(['GET'])
def save_financial_products(request):
    # ... (이전 답변의 전체 코드와 동일) ...
    api_key = settings.FSS_API_KEY
    if not api_key:
        return Response({'error': "금융감독원 API 키가 설정되지 않았습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    product_types_urls = {
        'deposit': 'depositProductsSearch.json',
        'saving': 'savingProductsSearch.json',
    }
    product_models = {'deposit': DepositProduct, 'saving': SavingProduct}
    option_models = {'deposit': DepositOption, 'saving': SavingOption}

    for p_type, url_suffix in product_types_urls.items():
        ProductModel = product_models[p_type]
        OptionModel = option_models[p_type]

        for dcls_month in dcls_months:
            api_url = f'http://finlife.fss.or.kr/finlifeapi/{url_suffix}?auth={api_key}&topFinGrpNo=020000&pageNo=1&dcls_month={dcls_month}'
            try:
                response_json = requests.get(api_url).json()
                if not response_json.get('result'):
                    print(f"{p_type} 상품 (월: {dcls_month}): API 결과 없음.")
                    continue

                base_list = response_json['result'].get('baseList', [])
                option_list = response_json['result'].get('optionList', [])

                ProductModel.objects.filter(dcls_month=dcls_month).delete()

                products_to_create = []
                for pd_data in base_list:
                    products_to_create.append(ProductModel(
                        fin_prdt_cd=pd_data['fin_prdt_cd'], kor_co_nm=pd_data['kor_co_nm'],
                        fin_prdt_nm=pd_data['fin_prdt_nm'], etc_note=pd_data.get('etc_note', ''),
                        join_deny=int(pd_data.get('join_deny', 0) or 0), join_member=pd_data.get('join_member', ''),
                        join_way=pd_data.get('join_way', ''), spcl_cnd=pd_data.get('spcl_cnd', ''),
                        dcls_month=pd_data.get('dcls_month'), fin_co_no=pd_data.get('fin_co_no'),
                        mtrt_int=pd_data.get('mtrt_int', ''), max_limit=pd_data.get('max_limit')
                    ))
                ProductModel.objects.bulk_create(products_to_create)
                
                options_to_create = []
                product_cache = {p.fin_prdt_cd: p for p in ProductModel.objects.filter(dcls_month=dcls_month)}

                for opt_data in option_list:
                    product_key = opt_data['fin_prdt_cd']
                    product_instance = product_cache.get(product_key)
                    
                    if product_instance and product_instance.fin_co_no == opt_data['fin_co_no']:
                        option_fields = {
                            f"{p_type}_product": product_instance,
                            'intr_rate_type': opt_data['intr_rate_type'], 'save_trm': opt_data['save_trm'],
                            'intr_rate_type_nm': opt_data['intr_rate_type_nm'],
                            'intr_rate': opt_data.get('intr_rate') if opt_data.get('intr_rate') is not None else -1.0,
                            'intr_rate2': opt_data.get('intr_rate2') if opt_data.get('intr_rate2') is not None else -1.0,
                        }
                        if p_type == 'saving':
                            option_fields['rsrv_type'] = opt_data['rsrv_type']
                            option_fields['rsrv_type_nm'] = opt_data['rsrv_type_nm']
                        options_to_create.append(OptionModel(**option_fields))
                    else:
                        print(f"Warning: {ProductModel.__name__} (월: {dcls_month}, 코드: {opt_data['fin_prdt_cd']}, 금융회사: {opt_data['fin_co_no']}) not found or fin_co_no mismatch. Skipping option.")
                if options_to_create:
                    OptionModel.objects.bulk_create(options_to_create)

            except requests.exceptions.RequestException as e: print(f"{p_type} API req err (월: {dcls_month}): {e}")
            except json.JSONDecodeError as e: print(f"{p_type} API JSON err (월: {dcls_month}): {e}")
            except Exception as e: print(f"{p_type} 데이터 처리 중 기타 err (월: {dcls_month}): {e}")
                
    return Response({"message": "금융 상품 정보 업데이트 완료."}, status=status.HTTP_200_OK)

# --- 예금/적금 상품 목록 및 상세 조회 뷰 ---
# (이전 답변의 deposit_products, deposit_product_detail, saving_products, saving_product_detail 함수와 동일하게 유지)
@api_view(['GET'])
def deposit_products(request):
    kor_co_nm = request.query_params.get('kor_co_nm')
    dcls_month = request.query_params.get('dcls_month')
    products_qs = DepositProduct.objects.all().prefetch_related('options')
    if kor_co_nm: products_qs = products_qs.filter(kor_co_nm__icontains=kor_co_nm)
    if dcls_month: products_qs = products_qs.filter(dcls_month=dcls_month)
    flat_products = []
    for product in products_qs:
        sorted_options = sorted(list(product.options.all()), key=lambda x: (x.save_trm is None, x.save_trm))
        for option in sorted_options:
            flat_products.append({
                'id': product.id, 'dcls_month': product.dcls_month, 'kor_co_nm': product.kor_co_nm,
                'fin_prdt_nm': product.fin_prdt_nm, 'save_trm': option.save_trm,
                'intr_rate': option.intr_rate, 'intr_rate2': option.intr_rate2,
                'intr_rate_type_nm': option.intr_rate_type_nm,
            })
    return Response(flat_products)

@api_view(['GET'])
def deposit_product_detail(request, pk):
    product = get_object_or_404(DepositProduct.objects.prefetch_related('options'), pk=pk)
    serializer = DepositProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def saving_products(request):
    kor_co_nm = request.query_params.get('kor_co_nm')
    dcls_month = request.query_params.get('dcls_month')
    products_qs = SavingProduct.objects.all().prefetch_related('options')
    if kor_co_nm: products_qs = products_qs.filter(kor_co_nm__icontains=kor_co_nm)
    if dcls_month: products_qs = products_qs.filter(dcls_month=dcls_month)
    flat_products = []
    for product in products_qs:
        sorted_options = sorted(list(product.options.all()), key=lambda x: (x.save_trm is None, x.save_trm))
        for option in sorted_options:
            flat_products.append({
                'id': product.id, 'dcls_month': product.dcls_month, 'kor_co_nm': product.kor_co_nm,
                'fin_prdt_nm': product.fin_prdt_nm, 'save_trm': option.save_trm,
                'intr_rate': option.intr_rate, 'intr_rate2': option.intr_rate2,
                'intr_rate_type_nm': option.intr_rate_type_nm, 'rsrv_type_nm': option.rsrv_type_nm,
            })
    return Response(flat_products)

@api_view(['GET'])
def saving_product_detail(request, pk):
    product = get_object_or_404(SavingProduct.objects.prefetch_related('options'), pk=pk)
    serializer = SavingProductSerializer(product)
    return Response(serializer.data)

# --- 상품 가입 뷰 ---
# (이전 답변의 subscribe_deposit_product, subscribe_saving_product 함수와 동일하게 유지)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_deposit_product(request, pk):
    product = get_object_or_404(DepositProduct, pk=pk)
    serializer = UserDepositSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, deposit_product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_saving_product(request, pk):
    product = get_object_or_404(SavingProduct, pk=pk)
    serializer = UserSavingSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, saving_product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# --- AI 상품 추천 (가입 상품 제외 기능 추가) ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ai_product_recommendations(request):
    user = request.user
    user_wealth = user.wealth if user.wealth is not None else 0
    user_age = user.age
    user_salary = user.salary

    # 사용자가 이미 가입한 예금 및 적금 상품 ID 목록 가져오기
    subscribed_deposit_ids = list(user.subscribed_deposit_products.values_list('id', flat=True))
    subscribed_saving_ids = list(user.subscribed_saving_products.values_list('id', flat=True))

    candidate_products_info = []

    # 예금 상품 필터링
    deposit_products_qs = DepositProduct.objects.prefetch_related('options').all()
    for product in deposit_products_qs:
        if product.id in subscribed_deposit_ids: # 이미 가입한 상품 제외
            continue

        eligible = False
        if product.join_deny == 1 or product.join_deny == 0: eligible = True
        elif user_wealth is not None:
            if product.join_deny == 2 and user_wealth <= 180000000: eligible = True
            elif product.join_deny == 3 and user_wealth >= 1000000000: eligible = True
        
        if eligible:
            valid_options = product.options.filter(intr_rate2__isnull=False).exclude(intr_rate2__lt=0)
            if valid_options.exists():
                max_rate = valid_options.aggregate(max_val=Max('intr_rate2'))['max_val']
                if max_rate is not None:
                    candidate_products_info.append({
                        'id': product.id, 'product_type': 'deposit', 'fin_prdt_nm': product.fin_prdt_nm,
                        'kor_co_nm': product.kor_co_nm, 'max_rate': float(max_rate),
                        'options': list(product.options.values('save_trm', 'intr_rate', 'intr_rate2')),
                        'spcl_cnd': product.spcl_cnd or "특별 조건 없음",
                    })

    # 적금 상품 필터링
    saving_products_qs = SavingProduct.objects.prefetch_related('options').all()
    for product in saving_products_qs:
        if product.id in subscribed_saving_ids: # 이미 가입한 상품 제외
            continue
            
        eligible = False
        if product.join_deny == 1 or product.join_deny == 0: eligible = True
        elif user_wealth is not None:
            if product.join_deny == 2 and user_wealth <= 180000000: eligible = True
            elif product.join_deny == 3 and user_wealth >= 1000000000: eligible = True
        
        if eligible:
            valid_options = product.options.filter(intr_rate2__isnull=False).exclude(intr_rate2__lt=0)
            if valid_options.exists():
                max_rate = valid_options.aggregate(max_val=Max('intr_rate2'))['max_val']
                if max_rate is not None:
                    candidate_products_info.append({
                        'id': product.id, 'product_type': 'saving', 'fin_prdt_nm': product.fin_prdt_nm,
                        'kor_co_nm': product.kor_co_nm, 'max_rate': float(max_rate),
                        'options': list(product.options.values('save_trm', 'intr_rate', 'intr_rate2', 'rsrv_type_nm')),
                        'spcl_cnd': product.spcl_cnd or "특별 조건 없음",
                    })

    candidate_products_info.sort(key=lambda x: x['max_rate'], reverse=True)
    top_candidates = candidate_products_info[:5] # OpenAI에 전달할 후보 상품 수 (최대 5개)

    if not top_candidates:
        return Response([], status=status.HTTP_200_OK)

    try:
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OpenAI API 키가 settings를 통해 로드되지 않았습니다.")
        client = OpenAI(api_key=api_key)
        
        user_profile_summary = f"사용자는 현재 자산 약 {user_wealth // 10000}만원"
        if user_age: user_profile_summary += f", 나이 {user_age}세"
        if user_salary: user_profile_summary += f", 연봉 약 {user_salary // 10000}만원"
        user_profile_summary += "입니다. 주로 안정적인 투자를 선호하며, 가능한 높은 이자율의 금융 상품에 관심이 많습니다. 이미 가입한 상품은 제외하고 추천 부탁드립니다." # 가입 상품 제외 요청 추가

        products_summary_for_openai = []
        for idx, p_info in enumerate(top_candidates):
            product_type_kor = "예금" if p_info['product_type'] == 'deposit' else "적금"
            options_desc_list = []
            for opt in p_info['options'][:2]:
                desc = f"{opt['save_trm']}개월"
                if p_info['product_type'] == 'saving' and opt.get('rsrv_type_nm'): desc += f"({opt['rsrv_type_nm']})"
                desc += f": 기본 {opt.get('intr_rate', 'N/A')}%, 우대 {opt.get('intr_rate2', 'N/A')}%"
                options_desc_list.append(desc)
            options_summary = "; ".join(options_desc_list) if options_desc_list else "옵션 정보 없음"
            spcl_cnd_summary = p_info.get('spcl_cnd', '특별 조건 없음')
            if spcl_cnd_summary and len(spcl_cnd_summary) > 80: spcl_cnd_summary = spcl_cnd_summary[:80] + '...'

            products_summary_for_openai.append(
                f"{idx+1}. 상품 ID: {p_info['id']}, \"{p_info['kor_co_nm']} - {p_info['fin_prdt_nm']}\" ({product_type_kor}), 최고 우대금리: {p_info['max_rate']:.2f}%, 주요 옵션: [{options_summary}], 우대조건(요약): \"{spcl_cnd_summary}\""
            )
        products_text = "\n".join(products_summary_for_openai)

        prompt = f"""
        당신은 고객의 금융 상황과 선호도에 맞춰 개인화된 금융 상품을 추천하는 AI 금융 전문가입니다.
        다음은 금융 상품 추천을 요청한 사용자의 정보와 추천 고려 대상 상품 목록입니다. 고객이 이미 가입한 상품은 추천에서 제외해야 합니다.

        고객 정보:
        {user_profile_summary}

        추천 고려 대상 상품 목록 (최대 5개, 금리 높은 순 정렬됨, 고객이 이미 가입한 상품은 이 목록에서 제외되었음):
        {products_text}

        위 고객 정보와 상품 목록을 면밀히 검토하여, 고객에게 가장 적합하다고 판단되는 상품을 **최대 2개까지** 선택해주십시오.
        각 추천 상품에 대해 다음 정보를 반드시 포함하는 JSON 객체를 생성하고, 이 객체들을 JSON 배열 형태로 응답해야 합니다:
        - "id": 상품의 고유 ID (숫자)
        - "fin_prdt_nm": 전체 상품명 (문자열)
        - "kor_co_nm": 금융 회사명 (문자열)
        - "product_type": "deposit" 또는 "saving" (문자열)
        - "max_rate": 해당 상품의 최고 우대 금리 (숫자, 소수점 둘째자리까지)
        - "recommendation_reason": 왜 이 상품이 고객에게 적합한지 구체적이고 설득력 있는 추천 이유 (한국어, 2-3문장 이내의 문자열)

        응답은 반드시 다른 설명 없이 요청된 JSON 배열만 반환해주십시오. 예를 들어 다음과 같습니다:
        [
          {{"id": 123, "fin_prdt_nm": "튼튼 예금", "kor_co_nm": "든든 은행", "product_type": "deposit", "max_rate": 3.50, "recommendation_reason": "고객님의 안정 선호 성향과 현재 자산 규모를 고려했을 때, 이 예금은 높은 이자율과 다양한 우대조건을 제공하여 매력적입니다. 특히 12개월 만기 시 제공되는 3.50%의 금리는 목돈 관리에 효과적일 것입니다."}}
        ]
        만약 추천할 상품이 없다면 빈 배열 []을 반환하십시오. 모든 필드명은 정확히 요청된 대로 작성해야 합니다.
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant that recommends products in Korean. Respond ONLY with the requested JSON array format. Ensure all floating point numbers for rates are formatted to two decimal places."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
        )
        response_content = chat_completion.choices[0].message.content
        
        if response_content:
            try:
                clean_response = response_content.strip()
                if clean_response.startswith("```json"): clean_response = clean_response[len("```json"):]
                if clean_response.endswith("```"): clean_response = clean_response[:-len("```")]
                clean_response = clean_response.strip()
                final_recommendations = json.loads(clean_response)
                if not isinstance(final_recommendations, list): final_recommendations = []

                processed_recommendations = []
                for rec_item in final_recommendations:
                    if isinstance(rec_item, dict) and all(key in rec_item for key in ['id', 'fin_prdt_nm', 'kor_co_nm', 'product_type', 'max_rate', 'recommendation_reason']):
                        try:
                            rec_item['id'] = int(rec_item['id'])
                            rec_item['max_rate'] = float(rec_item['max_rate'])
                            if rec_item['product_type'] not in ['deposit', 'saving']: continue
                            processed_recommendations.append(rec_item)
                        except (ValueError, TypeError) as e: print(f"AI 추천 항목 데이터 타입 변환 오류: {rec_item}, 오류: {e}")
                    else: print(f"AI 추천 항목 필수 필드 누락 또는 형식 오류: {rec_item}")
                return Response(processed_recommendations, status=status.HTTP_200_OK)
            except json.JSONDecodeError as e: print(f"OpenAI 응답 JSON 파싱 오류: {e}\n원본: {response_content}"); return Response({"error": "AI 결과 파싱 실패"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e: print(f"OpenAI 응답 처리 중 오류: {e}"); return Response({"error": "AI 결과 처리 중 오류"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: return Response([], status=status.HTTP_200_OK)
    except ValueError as ve: print(f"설정 오류: {str(ve)}"); return Response({"error": str(ve)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e: print(f"AI 추천 서비스 오류: {e}"); return Response({"error": f"AI 추천 중 오류: {str(e)}"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

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

def delete_saving_subscription(request, pk):
    """
    사용자가 가입한 적금 상품을 삭제(가입 취소)합니다.
    """
    subscription = get_object_or_404(UserSaving, pk=pk)
    if request.user != subscription.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    subscription.delete()
    return Response(data={'message': f'적금 가입 정보({pk})가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)