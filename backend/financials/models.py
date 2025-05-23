from django.db import models
from django.conf import settings

# 예금 상품
class DepositProduct(models.Model):
    interest_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interesting_deposits', blank=True)
    dcls_month = models.CharField(max_length=6, null=True, blank=True)
    fin_prdt_cd = models.CharField(max_length=50, null=True, blank=True)
    fin_co_no = models.CharField(max_length=50, null=True, blank=True)
    kor_co_nm = models.CharField(max_length=100, null=True, blank=True)
    fin_prdt_nm = models.CharField(max_length=150, null=True, blank=True)
    join_way = models.TextField(null=True, blank=True)
    mtrt_int = models.TextField(null=True, blank=True)
    spcl_cnd = models.TextField(null=True, blank=True)
    join_deny = models.SmallIntegerField(null=True, blank=True)
    join_member = models.TextField(null=True, blank=True)
    etc_note = models.TextField(null=True, blank=True)
    max_limit = models.BigIntegerField(null=True, blank=True)

# 예금 상품 옵션
class DepositOption(models.Model):
    deposit_product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='options')
    intr_rate_type = models.CharField(max_length=100, null=True, blank=True)
    intr_rate_type_nm = models.CharField(max_length=100, null=True, blank=True)
    save_trm = models.IntegerField(null=True, blank=True)
    intr_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    intr_rate2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

# 적금 상품
class SavingProduct(models.Model):
    interest_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interesting_savings', blank=True)
    dcls_month = models.CharField(max_length=6, null=True, blank=True)
    fin_prdt_cd = models.CharField(max_length=50, null=True, blank=True)
    fin_co_no = models.CharField(max_length=50, null=True, blank=True)
    kor_co_nm = models.CharField(max_length=100, null=True, blank=True)
    fin_prdt_nm = models.CharField(max_length=150, null=True, blank=True)
    join_way = models.TextField(null=True, blank=True)
    mtrt_int = models.TextField(null=True, blank=True)
    spcl_cnd = models.TextField(null=True, blank=True)
    join_deny = models.SmallIntegerField(null=True, blank=True)
    join_member = models.TextField(null=True, blank=True)
    etc_note = models.TextField(null=True, blank=True)
    max_limit = models.BigIntegerField(null=True, blank=True)

# 적금 상품 옵션
class SavingOption(models.Model):
    saving_product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE, related_name='options')
    intr_rate_type = models.CharField(max_length=100, null=True, blank=True)
    intr_rate_type_nm = models.CharField(max_length=100, null=True, blank=True)
    rsrv_type = models.CharField(max_length=50, null=True, blank=True)
    rsrv_type_nm = models.CharField(max_length=50, null=True, blank=True)
    save_trm = models.IntegerField(null=True, blank=True)
    intr_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    intr_rate2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


# 사용자-예금 상품 가입 정보 (중개 모델)
class UserDeposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deposit_product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE)
    signed_at = models.DateField(auto_now_add=True)
    maturity_at = models.DateField(null=True, blank=True)
    principal = models.BigIntegerField(default=0)
    applied_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'deposit_product', 'signed_at')


# 사용자-적금 상품 가입 정보 (중개 모델)
class UserSaving(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saving_product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE)
    signed_at = models.DateField(auto_now_add=True)
    maturity_at = models.DateField(null=True, blank=True)
    principal = models.BigIntegerField(default=0)
    applied_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'saving_product', 'signed_at')