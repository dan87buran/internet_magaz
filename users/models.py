from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = None

    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text='Обязательное поле. Укажите действующий email.'
    )

    avatar = models.ImageField(
        _('avatar'),
        upload_to='users/avatars/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text='Загрузите изображение вашего профиля'
    )

    phone = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        null=True,
        help_text='Номер телефона в формате +7 XXX XXX XX XX'
    )

    country = models.CharField(
        _('country'),
        max_length=100,
        blank=True,
        null=True,
        help_text='Страна проживания'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.email