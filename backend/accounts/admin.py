from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
# admin.site.register(User, UserAdmin) # 기본 UserAdmin 사용 시
# 또는 커스텀 UserAdmin을 정의하여 사용할 수 있습니다.

class CustomUserAdmin(UserAdmin):
    # UserAdmin의 기본 필드셋에 커스텀 필드 추가
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', 'subscribed_products')}),
    )
    # 관리자 페이지 목록에 표시할 필드 추가
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'age', 'subscribed_products')

admin.site.register(User, CustomUserAdmin)