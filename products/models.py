from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(
        _('name'),
        max_length=200,
        help_text='Название товара'
    )

    description = models.TextField(
        _('description'),
        blank=True,
        help_text='Подробное описание товара'
    )

    price = models.DecimalField(
        _('price'),
        max_digits=10,
        decimal_places=2,
        help_text='Цена в рублях'
    )

    image = models.ImageField(
        _('image'),
        upload_to='products/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text='Изображение товара'
    )

    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('owner')
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-created_at']

    def __str__(self):
        return self.name