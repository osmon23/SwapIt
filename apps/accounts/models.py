from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from apps.accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('Email'),
        unique=True,
    )
    phone_number = PhoneNumberField(
        _("Номер телефона"),
        max_length=100,
        unique=True
    )
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ('-id',)
