# backend/maps/urls.py
from django.urls import path
from . import views

app_name = 'maps'
urlpatterns = [
    path('kakao-key/', views.kakao_maps_api_key, name='kakao_maps_api_key'),
]