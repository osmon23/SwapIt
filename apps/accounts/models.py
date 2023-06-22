from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from apps.accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('Email'),
        unique=True,
        max_length=255,
    )
    phone_number = PhoneNumberField(
        _("Номер телефона"),
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True
    )
    rating = models.SmallIntegerField(
        _('Рейтинг'),
        default=0,
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


class Rating(models.Model):
    from_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='given_ratings',
        verbose_name=_('От пользователя')
    )
    to_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_ratings',
        verbose_name=_('К пользователю')
    )
    rating = models.SmallIntegerField(
        _('Рейтинг'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('Рейтинг')
        verbose_name_plural = _('Рейтинги')
        unique_together = ('from_user', 'to_user')
