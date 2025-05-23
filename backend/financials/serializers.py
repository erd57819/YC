from rest_framework import serializers
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption, UserDeposit, UserSaving

# 예금 옵션
class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        exclude = ('deposit_product',)

# 예금 상품
class DepositProductSerializer(serializers.ModelSerializer):
    options = DepositOptionSerializer(many=True, read_only=True)

    class Meta:
        model = DepositProduct
        fields = '__all__'


# 적금 옵션
class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        exclude = ('saving_product',)


# 적금 상품
class SavingProductSerializer(serializers.ModelSerializer):
    options = SavingOptionSerializer(many=True, read_only=True)

    class Meta:
        model = SavingProduct
        fields = '__all__'


# 사용자 예금 가입 정보
class UserDepositSerializer(serializers.ModelSerializer):
    deposit_product = DepositProductSerializer(read_only=True)

    class Meta:
        model = UserDeposit
        fields = '__all__'
        read_only_fields = ('user',)

# 사용자 적금 가입 정보
class UserSavingSerializer(serializers.ModelSerializer):
    saving_product = SavingProductSerializer(read_only=True)

    class Meta:
        model = UserSaving
        fields = '__all__'
        read_only_fields = ('user',)