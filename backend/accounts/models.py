from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    wealth = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    subscribed_saving_products = models.ManyToManyField('financials.SavingProduct', through='financials.UserSaving', related_name='subscribed_users')
    subscribed_deposit_products = models.ManyToManyField('financials.DepositProduct', through='financials.UserDeposit', related_name='subscribed_users')

    def __str__(self):
        return self.username