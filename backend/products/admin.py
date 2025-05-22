from django.contrib import admin
from .models import FinancialProduct, ProductOption

class ProductOptionInline(admin.TabularInline): # 또는 admin.StackedInline
    model = ProductOption
    extra = 1 # 기본으로 보여줄 빈 옵션 폼 개수

class FinancialProductAdmin(admin.ModelAdmin):
    list_display = ('fin_prdt_nm', 'kor_co_nm', 'product_type', 'dcls_strt_day')
    list_filter = ('product_type', 'kor_co_nm')
    search_fields = ('fin_prdt_nm', 'kor_co_nm', 'fin_prdt_cd')
    inlines = [ProductOptionInline] # 상품 등록/수정 페이지에서 옵션도 함께 관리

class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('get_product_name', 'save_trm', 'intr_rate_type_nm', 'intr_rate', 'intr_rate2')
    list_filter = ('intr_rate_type', 'product__kor_co_nm', 'product__product_type')
    search_fields = ('product__fin_prdt_nm', 'product__fin_prdt_cd')

    def get_product_name(self, obj):
        return obj.product.fin_prdt_nm
    get_product_name.short_description = '상품명' # Admin 페이지에 표시될 컬럼명

admin.site.register(FinancialProduct, FinancialProductAdmin)
admin.site.register(ProductOption, ProductOptionAdmin)