# products/management/commands/fetch_financial_products.py
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import FinancialProduct, ProductOption
from django.db import transaction

class Command(BaseCommand):
    help = 'Fetches financial product data from FinLife API and saves to DB'

    API_BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
    API_KEY = settings.FINLIFE_API_KEY # settings.py에 FINLIFE_API_KEY = env('FINLIFE_API_KEY') 추가 필요

    # API 엔드포인트 (예금, 적금)
    PRODUCT_ENDPOINTS = {
        'deposit': 'depositProductsSearch.json',
        'saving': 'savingProductsSearch.json',
    }

    def fetch_data_from_api(self, endpoint_url, params):
        try:
            response = requests.get(endpoint_url, params=params)
            response.raise_for_status() # 오류 발생 시 예외 발생
            return response.json()
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"API request failed: {e}"))
            return None
        except ValueError: # JSONDecodeError의 부모 클래스
            self.stderr.write(self.style.ERROR(f"Failed to decode JSON from response: {response.text}"))
            return None


    @transaction.atomic # 전체 작업을 하나의 트랜잭션으로 묶음
    def handle_product_data(self, product_data_list, product_options_list, product_type):
        saved_count = 0
        skipped_count = 0
        options_saved_count = 0

        # 상품 기본 정보 저장
        for product_item in product_data_list:
            fin_prdt_cd = product_item.get('fin_prdt_cd')
            if not fin_prdt_cd:
                self.stderr.write(self.style.WARNING(f"Skipping product due to missing fin_prdt_cd: {product_item.get('fin_prdt_nm')}"))
                continue

            # 이미 존재하는 데이터는 새로 저장하지 않도록 구성 (fin_prdt_cd 기준)
            product, created = FinancialProduct.objects.update_or_create(
                fin_prdt_cd=fin_prdt_cd,
                defaults={
                    'kor_co_nm': product_item.get('kor_co_nm'),
                    'fin_prdt_nm': product_item.get('fin_prdt_nm'),
                    'etc_note': product_item.get('etc_note'),
                    'join_deny': product_item.get('join_deny'),
                    'join_member': product_item.get('join_member'),
                    'join_way': product_item.get('join_way'),
                    'spcl_cnd': product_item.get('spcl_cnd'),
                    'mtrt_int': product_item.get('mtrt_int'),
                    'max_limit': product_item.get('max_limit'),
                    'dcls_strt_day': product_item.get('dcls_strt_day'),
                    'dcls_end_day': product_item.get('dcls_end_day'),
                    'fin_co_subm_day': product_item.get('fin_co_subm_day'),
                    'product_type': product_type,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Saved new product: {product.fin_prdt_nm}"))
                saved_count += 1
            else:
                self.stdout.write(f"Updated existing product: {product.fin_prdt_nm}")
                skipped_count +=1 # update_or_create는 업데이트도 포함하므로, 실제로는 업데이트 카운트
            
            # 해당 상품의 기존 옵션 삭제 후 새로 추가 (또는 더 정교한 업데이트 로직 구현)
            # ProductOption.objects.filter(product=product).delete() # 간단하게는 이렇게 처리

        # 상품 옵션 정보 저장
        for option_item in product_options_list:
            fin_prdt_cd_opt = option_item.get('fin_prdt_cd')
            if not fin_prdt_cd_opt:
                continue
            
            try:
                related_product = FinancialProduct.objects.get(fin_prdt_cd=fin_prdt_cd_opt, product_type=product_type)
            except FinancialProduct.DoesNotExist:
                self.stderr.write(self.style.WARNING(f"No matching product found for option with fin_prdt_cd: {fin_prdt_cd_opt}. Skipping option."))
                continue

            # 옵션도 update_or_create 사용 가능 (save_trm, intr_rate_type 등으로 고유성 판단)
            # 여기서는 기존 옵션을 삭제하고 새로 추가하는 대신, 각 옵션의 고유성을 기반으로 update_or_create
            option_defaults = {
                'intr_rate_type': option_item.get('intr_rate_type'),
                'intr_rate_type_nm': option_item.get('intr_rate_type_nm'),
                'intr_rate': option_item.get('intr_rate'),
                'intr_rate2': option_item.get('intr_rate2'),
            }
            # save_trm 값이 null이거나 빈 문자열인 경우 처리
            save_trm_value = option_item.get('save_trm')
            if not save_trm_value: # 또는 if save_trm_value is None or save_trm_value == '':
                self.stderr.write(self.style.WARNING(f"Skipping option for {related_product.fin_prdt_nm} due to missing save_trm."))
                continue


            option, created = ProductOption.objects.update_or_create(
                product=related_product,
                fin_prdt_cd=fin_prdt_cd_opt, # FinancialProduct의 fin_prdt_cd와 동일하게 저장
                save_trm=save_trm_value, # 이 필드가 고유성 판단에 중요
                intr_rate_type=option_item.get('intr_rate_type'), # 단/복리 유형도 고유성 판단에 포함 가능
                defaults=option_defaults
            )
            
            if created:
                options_saved_count += 1

        self.stdout.write(self.style.SUCCESS(f"{product_type.capitalize()} - Products saved: {saved_count}, Products updated/skipped: {skipped_count}, Options saved/updated: {options_saved_count}"))


    def handle(self, *args, **options):
        self.stdout.write("Fetching financial product data...")
        
        # 금융회사 코드 목록 (020000: 은행, 030200: 여신전문, 030300: 저축은행, 050000: 보험, 060000: 금투)
        # 요구사항에 따라 은행만 가져오거나 전체를 가져올 수 있음. 예시에서는 전체 은행.
        # API 명세에 따라 'topFinGrpNo' 파라미터 사용 (020000: 은행, 030300: 저축은행 등)
        # 여기서는 모든 금융권역(은행, 저축은행) 데이터를 가져오는 것으로 가정
        # 실제 API는 페이지네이션이 필요할 수 있으므로, 한 번에 모든 데이터를 가져오지 못할 경우 반복 처리 필요.
        # 금융감독원 API는 pageNo 파라미터가 있으나, 한 번에 모든 은행 데이터를 주는지 확인 필요.
        # 여기서는 일단 topFinGrpNo 없이 전체를 가져오는 것으로 가정
        
        financial_corps = ['020000'] # 은행만 가져오도록 수정 (요구사항 해석에 따라 변경)
        # financial_corps = ['020000', '030300'] # 은행 및 저축은행
        
        for product_key, endpoint in self.PRODUCT_ENDPOINTS.items():
            self.stdout.write(self.style.HTTP_INFO(f"Fetching {product_key}..."))
            url = f"{self.API_BASE_URL}{endpoint}"
            
            for corp_num in financial_corps:
                params = {
                    'auth': self.API_KEY,
                    'topFinGrpNo': corp_num, 
                    'pageNo': 1 
                    # 금융감독원 API는 결과 건수가 많을 경우 pageNo를 증가시켜 여러번 호출해야 할 수 있음
                    # 여기서는 1페이지만 가져오는 것으로 단순화 (실제 구현 시 반복 로직 추가 필요)
                }
                
                data = self.fetch_data_from_api(url, params)

                if data and data.get('result'):
                    base_list = data['result'].get('baseList', [])
                    option_list = data['result'].get('optionList', [])
                    
                    if not base_list:
                        self.stdout.write(self.style.WARNING(f"No baseList found for {product_key} in {corp_num}"))
                        continue
                    if not option_list:
                         self.stdout.write(self.style.WARNING(f"No optionList found for {product_key} in {corp_num}"))
                        # 옵션이 없는 상품도 있을 수 있으므로, baseList는 처리하도록 함.

                    self.handle_product_data(base_list, option_list, product_key)
                else:
                    self.stderr.write(self.style.ERROR(f"No data received or error in data for {product_key} in {corp_num}"))

        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved all financial product data.'))