# backend/accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    # ... (기존 코드와 동일)
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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'age', 'salary', 'wealth', 'created_at', 'updated_at') # 'user_id' -> 'id'
        read_only_fields = ('username', 'created_at', 'updated_at')
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲