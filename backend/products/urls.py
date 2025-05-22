from django.urls import path
from . import views

app_name = 'products' # 앱 네임스페이스 추가

urlpatterns = [
    path('', views.product_list, name='product_list'), # /api/v1/products/
    path('<str:product_pk_or_code>/', views.product_detail, name='product_detail'), # /api/v1/products/{pk_or_code}/
    path('<str:product_pk_or_code>/subscribe/', views.subscribe_product, name='subscribe_product'), # /api/v1/products/{pk_or_code}/subscribe/
    path('<str:product_pk_or_code>/unsubscribe/', views.unsubscribe_product, name='unsubscribe_product'), # /api/v1/products/{pk_or_code}/unsubscribe/
]