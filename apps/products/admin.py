from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import Category, Product


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
