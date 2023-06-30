from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey


User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(
        _('Название'),
        max_length=255
    )
    parent = TreeForeignKey(
        'self',
        verbose_name=_('Родительская категория'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return f"{self.name}"

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class Product(models.Model):
    name = models.CharField(
        _('Название'),
        max_length=255
    )
    description = models.TextField(
        _('Описание'),
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(
        _('Количество в наличий'),
        default=1
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_('Категория'),
        related_name='products',
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Создано пользователем'),
        related_name='created_products',
        null=True,
        blank=True,
    )
    image = models.ImageField(
        _('Image'),
        upload_to='images/'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')
