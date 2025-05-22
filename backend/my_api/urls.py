# backend/my_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/articles/', include('articles.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/maps/', include('maps.urls')), # 추가
    path('accounts/', include('dj_rest_auth.urls')),
    path('api/v1/recommendations/', include('recommendations.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
]