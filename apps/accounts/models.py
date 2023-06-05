from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('Email'),
        unique=True,
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=255,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=255,
        null=True,
        blank=True,
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
