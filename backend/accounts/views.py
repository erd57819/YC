from django.shortcuts import render

# Create your views here.
# backend/maps/views.py
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny]) # API 키 요청은 인증 불필요
def kakao_maps_api_key(request):
    """
    Kakao Maps JavaScript API 키를 반환합니다.
    """
    api_key = getattr(settings, 'KAKAO_API_KEY', None)
    if not api_key:
        return Response({'error': 'Kakao API Key not configured in settings.'}, status=500)
    return Response({'kakao_api_key': api_key})