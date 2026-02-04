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
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликован',
        help_text='Отметьте для публикации товара'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='products',
        null=True,  # Для существующих записей
        blank=True  # Для форм
    )


    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-created_at']

    class Meta:
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
            ('can_change_category', 'Может изменять категорию продукта'),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name