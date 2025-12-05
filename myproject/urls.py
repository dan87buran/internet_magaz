from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("Главная страница работает!")

def contacts(request):
    return HttpResponse("Страница контактов работает!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('contacts/', contacts),
]