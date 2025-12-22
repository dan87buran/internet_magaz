from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductForm


# Главная страница - ListView
class ProductListView(ListView):
    """Список товаров на главной странице"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        """Получаем только товары с сортировкой по дате создания"""
        return Product.objects.all().order_by('-created_at')


# Страница товара - DetailView
class ProductDetailView(DetailView):
    """Детальная страница товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


# Страница контактов - TemplateView
class ContactsView(TemplateView):
    """Страница контактов"""
    template_name = 'catalog/contacts.html'


# Создание товара - CreateView (дополнительное задание из прошлой работы)
class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового товара"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Дополнительная обработка при успешном создании"""
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# Редактирование товара - UpdateView (дополнительное задание из прошлой работы)
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        """После успешного редактирования переходим на страницу товара"""
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})