from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings

from .forms import UserRegisterForm, UserLoginForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Сохраняем пользователя
        user = form.save()

        # Отправляем приветственное письмо
        self.send_welcome_email(user)

        # Авторизуем пользователя
        login(self.request, user)

        # Добавляем сообщение об успехе
        messages.success(
            self.request,
            f'Добро пожаловать, {user.email}! Регистрация прошла успешно.'
        )

        return redirect(self.success_url)

    def send_welcome_email(self, user):
        subject = 'Добро пожаловать в наш интернет-магазин!'
        message = f'''
        Уважаемый(ая) {user.email},

        Добро пожаловать в наш интернет-магазин!

        Спасибо за регистрацию. Теперь вы можете:
        • Просматривать все товары
        • Создавать и управлять своими товарами
        • Пользоваться всеми преимуществами нашего сервиса

        Если у вас возникнут вопросы, свяжитесь с нашей службой поддержки.

        С уважением,
        Команда интернет-магазина
        '''

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next', '')
        if next_url:
            return next_url
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно вошли в систему.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка входа. Проверьте email и пароль.')
        return super().form_invalid(form)