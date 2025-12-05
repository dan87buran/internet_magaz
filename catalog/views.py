from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    """Контроллер главной страницы"""
    return render(request, 'catalog/home.html')


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