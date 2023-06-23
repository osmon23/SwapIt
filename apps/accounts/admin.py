from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'username',
        'rating',
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


admin.site.register(CustomUser, CustomUserAdmin)
