from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    # 기존 필드 외에 추가할 필드를 정의합니다.
    nickname = serializers.CharField(max_length=20, required=False)
    age = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)
    wealth = serializers.IntegerField(required=False)

    def get_cleaned_data(self):
        # 기본 'get_cleaned_data' 메소드를 호출하여 cleaned_data를 가져옵니다.
        data = super().get_cleaned_data()
        # 추가한 필드들을 cleaned_data에 추가합니다.
        data['nickname'] = self.validated_data.get('nickname', '')
        data['age'] = self.validated_data.get('age', None)
        data['salary'] = self.validated_data.get('salary', None)
        data['wealth'] = self.validated_data.get('wealth', None)
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'nickname', 'age', 'salary', 'wealth', 'created_at', 'updated_at')
        read_only_fields = ('username', 'created_at', 'updated_at')