# backend/recommendations/urls.py
from django.urls import path
from . import views

app_name = 'recommendations'
urlpatterns = [
    path('', views.get_basic_recommendations, name='get_recommendations'),
]