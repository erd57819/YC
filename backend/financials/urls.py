from django.urls import path
from . import views

urlpatterns = [
    # API 데이터를 DB에 저장하기 위한 URL
    path('save-products/', views.save_financial_products),

    # 예금 상품 목록 및 상세 정보 URL
    path('deposit-products/', views.deposit_products),
    path('deposit-products/<int:pk>/', views.deposit_product_detail),
    path('deposit-products/<int:pk>/subscribe/', views.subscribe_deposit_product), # 예금 상품 가입 URL

    # 적금 상품 목록 및 상세 정보 URL
    path('saving-products/', views.saving_products),
    path('saving-products/<int:pk>/', views.saving_product_detail),
    path('saving-products/<int:pk>/subscribe/', views.subscribe_saving_product), # 적금 상품 가입 URL
    # path('subscriptions/deposits/<int:pk>/', views.delete_deposit_subscription),
    # path('subscriptions/savings/<int:pk>/', views.delete_saving_subscription),
    path('ai-recommendations/', views.ai_product_recommendations, name='ai_product_recommendations'),
]