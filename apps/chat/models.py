from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(
        User,
        related_name='friends',
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE,
    )
    friends = models.ManyToManyField(
        'self',
        verbose_name=_('Собеседник'),
        blank=True,
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Контакт')
        verbose_name_plural = _('Контакты')


class Message(models.Model):
    contact = models.ForeignKey(
        Contact,
        related_name='messages',
        verbose_name=_('Контакт'),
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        _('Сообщение'),
    )
    timestamp = models.DateTimeField(
        _('Время отправки'),
        auto_now_add=True
    )

    def __str__(self):
        return self.contact.user.username

    class Meta:
        verbose_name = _('Сообщение')
        verbose_name_plural = _('Сообщения')


class Chat(models.Model):
    participants = models.ManyToManyField(
        Contact,
        verbose_name=_('Участники'),
        related_name='chats',
        blank=True,
    )
    messages = models.ManyToManyField(
        Message,
        verbose_name=_('Сообщение'),
        blank=True,
    )

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = _('Чат')
        verbose_name_plural = _('Чаты')
