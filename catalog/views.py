from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.urls import reverse
from .forms import ProductForm
from .models import Product, Category


@login_required
@permission_required('catalog.can_publish_product', raise_exception=True)
def product_create(request):
    """Создание нового продукта"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Товар "{product.name}" успешно создан!')
            return redirect('product_detail', pk=product.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'title': 'Создание нового товара',
        'submit_text': 'Создать товар'
    }
    return render(request, 'catalog/product_form.html', context)


@login_required
@permission_required('catalog.can_publish_product', raise_exception=True)
def product_update(request, pk):
    """Редактирование существующего продукта"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Товар "{product.name}" успешно обновлен!')
            return redirect('product_detail', pk=product.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'title': 'Редактирование товара',
        'submit_text': 'Сохранить изменения',
        'product': product
    }
    return render(request, 'catalog/product_form.html', context)


@login_required
@permission_required('catalog.can_publish_product', raise_exception=True)
def product_delete(request, pk):
    """Удаление продукта"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Товар "{product_name}" успешно удален!')
        return redirect('home')

    context = {
        'product': product,
        'title': 'Удаление товара'
    }
    return render(request, 'catalog/product_confirm_delete.html', context)


def product_list(request):
    """Список всех опубликованных продуктов"""
    products = Product.objects.filter(is_published=True).order_by('-created_at')

    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'current_category': category_id,
        'search_query': search_query
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, pk):
    """Детальная информация о продукте"""
    product = get_object_or_404(Product, pk=pk)

    # Проверка прав на просмотр неопубликованных товаров
    if not product.is_published and not request.user.has_perm('catalog.can_publish_product'):
        messages.error(request, 'Этот товар еще не опубликован.')
        return redirect('home')

    context = {
        'product': product
    }
    return render(request, 'catalog/product_detail.html', context)