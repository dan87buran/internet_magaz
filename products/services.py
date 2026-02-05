from django.core.cache import cache
from django.conf import settings
from .models import Product, Category


def get_products_by_category(category_id):
    """
    Сервисная функция для получения продуктов по категории с кешированием
    """
    if settings.CACHE_ENABLED:
        cache_key = f'products_category_{category_id}'
        products = cache.get(cache_key)

        if products is not None:
            return products

        products = Product.objects.filter(
            category_id=category_id,
            is_published=True
        ).select_related('owner', 'category')

        cache.set(cache_key, products, settings.CACHE_TTL)
        return products
    else:
        return Product.objects.filter(
            category_id=category_id,
            is_published=True
        ).select_related('owner', 'category')


def get_all_products_cached():
    """
    Низкоуровневое кеширование списка всех продуктов
    """
    if settings.CACHE_ENABLED:
        cache_key = 'all_products_list'
        products = cache.get(cache_key)

        if products is not None:
            return products

        products = Product.objects.filter(
            is_published=True
        ).select_related('owner', 'category').prefetch_related('category')

        cache.set(cache_key, products, settings.CACHE_TTL)
        return products
    else:
        return Product.objects.filter(is_published=True)


def invalidate_products_cache():
    """
    Инвалидация кеша продуктов
    Используется при создании/обновлении/удалении продуктов
    """
    if settings.CACHE_ENABLED:
        cache.delete('all_products_list')
        print("Кеш продуктов очищен")