from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
    )
    list_display_links = (
        'indented_title',
    )
    list_filter = (
        'parent',
    )
    search_fields = (
        'title',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'quantity',
        'category',
        'description',
    )
    list_filter = (
        'category',
    )
    search_fields = (
        'name',
        'description',
    )
    inlines = (
        ProductImageInline,
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        'image',
        'product',
    )
    list_filter = (
        'product',
    )
    search_fields = (
        'product__name',
    )
