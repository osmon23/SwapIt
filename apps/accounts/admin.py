from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserManagerAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'phone_number',
        'created_at',
    )
    search_fields = (
        'email',
        'username',
    )
    ordering = (
        'email',
    )
    exclude = (
        'password',
    )
