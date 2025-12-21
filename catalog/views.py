from django.db import models
from django.shortcuts import render, get_object_or_404


def product_detail(request, pk):
    """Контроллер для отображения страницы одного товара"""
    product = get_object_or_404(models.Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'catalog/product_detail.html', context)


def home(request):
    """Главная страница со списком товаров"""
    products = models.Product.objects.all().order_by('-created_at')

    context = {
        'products': products,
    }
    return render(request, 'catalog/home.html', context)

def contacts(request):
    """Контроллер страницы контактов"""
    context = {}

    if request.method == 'POST':
        # Обработка данных формы
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Здесь можно добавить логику обработки формы,
        # например, сохранение в базу данных или отправку email

        context['success'] = True
        context['name'] = name

    return render(request, 'catalog/contacts.html', context)


def views():
    return None