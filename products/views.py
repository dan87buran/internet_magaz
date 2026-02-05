from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.conf import settings
from products.services import get_products_by_category, get_all_products_cached, invalidate_products_cache
from models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        # Используем сервисную функцию с кешированием
        return get_all_products_cached()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        if settings.CACHE_ENABLED:
            context['cache_enabled'] = True
            context['cache_ttl'] = settings.CACHE_TTL // 60
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


class CategoryProductsView(ListView):
    model = Product
    template_name = 'products/category_products.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context['category'] = Category.objects.get(id=category_id)

        if settings.CACHE_ENABLED:
            cache_key = f'products_category_{category_id}'
            cached = cache.get(cache_key) is not None
            context['cached'] = cached
            context['cache_enabled'] = True

        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description', 'price', 'image', 'category', 'is_published']
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        if settings.CACHE_ENABLED:
            invalidate_products_cache()
        return response


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description', 'price', 'image', 'category']

    def form_valid(self, form):
        response = super().form_valid(form)
        if settings.CACHE_ENABLED:
            invalidate_products_cache()
        return response


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if settings.CACHE_ENABLED:
            invalidate_products_cache()
        return response


class ProductModerationView:
    pass