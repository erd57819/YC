# backend/golds/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.gold_list),         # /golds/ 요청 시 금 데이터 반환
    path('silver/', views.silver_list), # /golds/silver/ 요청 시 은 데이터 반환
]