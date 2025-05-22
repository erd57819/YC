from django.db import models

# 은행 정보 (선택 사항이지만, API 응답에 따라 필요할 수 있음)
# class Bank(models.Model):
#     bank_code = models.CharField(max_length=20, unique=True) # 금융회사 코드
#     kor_co_nm = models.CharField(max_length=100) # 금융회사 명
#     # ... 기타 은행 정보

#     def __str__(self):
#         return self.kor_co_nm

class FinancialProduct(models.Model):
    PRODUCT_TYPES = [
        ('deposit', '예금'),
        ('saving', '적금'),
    ]
    
    fin_prdt_cd = models.CharField(max_length=100, unique=True)  # 금융 상품 코드 (API의 fin_prdt_cd)
    kor_co_nm = models.CharField(max_length=100)  # 금융 회사명
    fin_prdt_nm = models.CharField(max_length=255)  # 금융 상품명
    etc_note = models.TextField(null=True, blank=True)  # 금융 상품 설명
    join_deny = models.IntegerField(choices=[(1, '제한없음'), (2, '서민전용'), (3, '일부제한')], null=True, blank=True) # 가입제한 (1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField(null=True, blank=True)  # 가입 대상
    join_way = models.TextField(null=True, blank=True)  # 가입 방법
    spcl_cnd = models.TextField(null=True, blank=True)  # 우대 조건
    
    mtrt_int = models.TextField(null=True, blank=True) # 만기 후 이자율
    max_limit = models.BigIntegerField(null=True, blank=True) # 최고한도
    
    dcls_strt_day = models.CharField(max_length=8, null=True, blank=True) # 공시 시작일 (YYYYMMDD)
    dcls_end_day = models.CharField(max_length=8, null=True, blank=True) # 공시 종료일 (YYYYMMDD)
    fin_co_subm_day = models.CharField(max_length=12, null=True, blank=True) # 금융회사 제출일 (YYYYMMDDHHMM)
    
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPES, default='deposit') # 상품 유형 (예금/적금)

    # bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='products', null=True) # 은행 모델 연동 시

    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm} ({self.get_product_type_display()})"

class ProductOption(models.Model):
    product = models.ForeignKey(FinancialProduct, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.CharField(max_length=100) # 연결된 금융 상품 코드 (중복 가능, 부모를 따름)
    intr_rate_type = models.CharField(max_length=1)  # 저축 금리 유형 (S:단리, M:복리)
    intr_rate_type_nm = models.CharField(max_length=10) # 저축 금리 유형명
    save_trm = models.CharField(max_length=3)  # 저축 기간 (개월)
    intr_rate = models.FloatField(null=True, blank=True)  # 저축 금리 (기본)
    intr_rate2 = models.FloatField(null=True, blank=True) # 최고 우대 금리

    class Meta:
        # 상품 코드와 옵션(기간, 금리유형)의 조합은 고유해야 할 수 있음 (API 데이터 구조에 따라 결정)
        # unique_together = [['product', 'save_trm', 'intr_rate_type']]
        ordering = ['save_trm'] # 저축 기간 순으로 정렬

    def __str__(self):
        return f"{self.product.fin_prdt_nm} - {self.save_trm}개월 ({self.intr_rate_type_nm}): 기본 {self.intr_rate}%, 우대 {self.intr_rate2}%"