from django.urls import path
from . import views

# articles/url.py

urlpatterns = [
    path('', views.article_list),  # 'articles/'를 ''로 변경
    path('<int:article_pk>/', views.article_detail), # 상세 페이지 경로는 article_pk만 남김 (기존 articles/ 삭제)
]