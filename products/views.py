from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView,
    DeleteView, DetailView
)
from .models import Product


# Общедоступный просмотр списка товаров
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10


# Защищенные действия требуют авторизации
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description', 'price', 'image']
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description', 'price', 'image']

    def get_success_url(self):
        return reverse_lazy('product_list')

    def get_queryset(self):
        # Пользователь может редактировать только свои товары
        return super().get_queryset().filter(owner=self.request.user)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        # Пользователь может удалять только свои товары
        return super().get_queryset().filter(owner=self.request.user)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'