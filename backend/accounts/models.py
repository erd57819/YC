from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    subscribed_products = models.TextField(blank=True, null=True) # 가입한 상품 목록 (쉼표로 구분된 ID)
    
    # 추가된 필드
    annual_salary = models.BigIntegerField(blank=True, null=True, verbose_name='연봉')
    current_assets = models.BigIntegerField(blank=True, null=True, verbose_name='현재 가진 금액')

    def __str__(self):
        return self.username