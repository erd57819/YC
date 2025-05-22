# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    age = models.PositiveIntegerField(blank=True, null=True)
    # email 필드는 AbstractUser에 이미 존재합니다.
    # USERNAME_FIELD를 'email'로 변경하고 싶다면 추가 설정이 필요하지만,
    # 여기서는 username을 기본으로 사용하고 email도 필수로 받도록 하겠습니다.
    email = models.EmailField(blank=False, null=False, unique=True) # 이메일 필수를 위해 blank=False, unique=True 추가
    subscribed_products = models.TextField(blank=True, null=True) # 가입한 상품 목록 (쉼표로 구분된 ID)

    def __str__(self):
        return self.username