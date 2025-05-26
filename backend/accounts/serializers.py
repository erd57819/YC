from django.db import transaction
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from financials.serializers import UserDepositSerializer, UserSavingSerializer

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=20, required=False)
    age = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)
    wealth = serializers.IntegerField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['age'] = self.validated_data.get('age', None)
        data['salary'] = self.validated_data.get('salary', None)
        data['wealth'] = self.validated_data.get('wealth', None)
        return data
    
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        
        user.nickname = self.validated_data.get('nickname', None)
        user.age = self.validated_data.get('age', None)
        user.salary = self.validated_data.get('salary', None)
        user.wealth = self.validated_data.get('wealth', None)
        
        user.save()
        
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    subscribed_deposits = UserDepositSerializer(source='userdeposit_set', many=True, read_only=True)
    subscribed_savings = UserSavingSerializer(source='usersaving_set', many=True, read_only=True)

    class Meta:
        model = User
        # Meta.fields에 'subscribed_deposits'와 'subscribed_savings'를 명시적으로 추가해야 합니다.
        fields = (
            'id', 
            'username', 
            'nickname', 
            'age', 
            'salary', 
            'wealth', 
            'subscribed_deposits',  # 여기에 추가
            'subscribed_savings',   # 여기에 추가
            'created_at', 
            'updated_at'
        )
        read_only_fields = ('username', 'created_at', 'updated_at')