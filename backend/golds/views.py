# backend/golds/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Gold, Silver
from .serializers import GoldSerializer, SilverSerializer

@api_view(['GET'])
def gold_list(request):
    """
    모든 금 시세 데이터를 조회하여 반환합니다.
    """
    golds = Gold.objects.all()
    serializer = GoldSerializer(golds, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def silver_list(request):
    """
    모든 은 시세 데이터를 조회하여 반환합니다.
    """
    silvers = Silver.objects.all()
    serializer = SilverSerializer(silvers, many=True)
    return Response(serializer.data)