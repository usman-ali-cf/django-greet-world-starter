from django.contrib import admin
from .models import (
    ProductCategory, 
    ProductSubCategory, 
    ProductType, 
    AgeCategory, 
    IFRACategory, 
    Product, 
    AllowedProductTypeByAge, 
    FrameFormulation, 
    IngredientType
)


class ProductSubCategoryInline(admin.TabularInline):
    model = ProductSubCategory
    extra = 1
    fields = ('unique_id', 'code', 'name', 'sub_category_num')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'code', 'name', 'category_num')
    search_fields = ('unique_id', 'code', 'name', 'category_num')
    list_filter = ('category_num',)
    inlines = [ProductSubCategoryInline]


class ProductTypeInline(admin.TabularInline):
    model = ProductType
    extra = 1
    fields = ('unique_id', 'code', 'name', 'estimated_daily_amount_applied_qx')


@admin.register(ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'code', 'name', 'sub_category_num', 'sccs_product_category')
    search_fields = ('unique_id', 'code', 'name', 'sub_category_num')
    list_filter = ('sccs_product_category', 'sub_category_num')


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = (
        'unique_id',
        'code',
        'name',
        'sccs_prod_cat',
        'estimated_daily_amount_applied_qx',
        'relative_daily_amount_applied_qx',
        'retention_factor_fret',
        'frequency_of_application'
    )
    search_fields = ('unique_id', 'code', 'name')
    list_filter = ('sccs_prod_cat',)
    fieldsets = (
        (None, {
            'fields': ('unique_id', 'code', 'name', 'sccs_prod_cat')
        }),
        ('Exposure Parameters', {
            'fields': (
                'estimated_daily_amount_applied_qx',
                'relative_daily_amount_applied_qx',
                'retention_factor_fret',
                'calculated_daily_exposure_product',
                'calculated_relative_daily_exposure_product',
                'frequency_of_application',
                'surface_area_for_application'
            )
        }),
    )


@admin.register(AgeCategory)
class AgeCategoryAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'category', 'body_weight', 'surface_area')
    search_fields = ('unique_id', 'category')
    list_filter = ('category',)


@admin.register(IFRACategory)
class IFRACategoryAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'code', 'category', 'type_of_prod', 'description')
    search_fields = ('unique_id', 'code', 'category', 'type_of_prod', 'description')
    list_filter = ('category', 'type_of_prod')


class AllowedProductTypeByAgeInline(admin.TabularInline):
    model = AllowedProductTypeByAge
    extra = 1
    fields = ('unique_id', 'age_category')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'unique_id',
        'product_name',
        'sccs_primary_prod_type',
        'age_category',
        'primary_exposure_route',
        'foreseeable_exposure_route',
        'ifra_ora_category',
        'sccs_secondary_prod_type',
        'leave_on_or_rinse_off_status'
    )
    search_fields = ('unique_id', 'product_name', 'primary_exposure_route', 'foreseeable_exposure_route')
    list_filter = (
        'sccs_primary_prod_type',
        'age_category',
        'ifra_ora_category',
        'sccs_secondary_prod_type',
        'leave_on_or_rinse_off_status'
    )
    fieldsets = (
        (None, {
            'fields': ('unique_id', 'product_name')
        }),
        ('Product Classification', {
            'fields': (
                'sccs_primary_prod_type',
                'sccs_secondary_prod_type',
                'age_category',
                'ifra_ora_category',
            )
        }),
        ('Exposure Information', {
            'fields': (
                'primary_exposure_route',
                'foreseeable_exposure_route',
                'leave_on_or_rinse_off_status',
            )
        }),
    )
    inlines = [AllowedProductTypeByAgeInline]


@admin.register(AllowedProductTypeByAge)
class AllowedProductTypeByAgeAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'sccs_product', 'age_category')
    search_fields = ('unique_id',)
    list_filter = ('sccs_product', 'age_category')


class IngredientTypeInline(admin.TabularInline):
    model = IngredientType
    extra = 1
    fields = ('unique_id', 'type', 'example', 'concentration')


@admin.register(FrameFormulation)
class FrameFormulationAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'name', 'link', 'sccs_product_sub_cat', 'formulation_num')
    search_fields = ('unique_id', 'name', 'formulation_num')
    list_filter = ('sccs_product_sub_cat',)
    inlines = [IngredientTypeInline]


@admin.register(IngredientType)
class IngredientTypeAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'type', 'example', 'concentration', 'frame_formulation')
    search_fields = ('unique_id', 'type', 'example')
    list_filter = ('frame_formulation', 'type')
