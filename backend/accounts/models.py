from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 기존 필드: username, password, age 등 AbstractUser의 필드와 이전 User 모델의 age 필드
    nickname = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    wealth = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # User와 SavingProduct/DepositProduct 간의 관계
    # 'through' 옵션으로 중개 모델을 지정합니다.
    subscribed_saving_products = models.ManyToManyField('financials.SavingProduct', through='financials.UserSaving', related_name='subscribed_users')
    subscribed_deposit_products = models.ManyToManyField('financials.DepositProduct', through='financials.UserDeposit', related_name='subscribed_users')

    def __str__(self):
        return self.username