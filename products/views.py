from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView



class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description', 'price', 'image', 'is_published']
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):

        form.instance.owner = self.request.user
        return super().form_valid(form)



class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description', 'price', 'image']

    def get_queryset(self):

        return super().get_queryset().filter(owner=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if not self.request.user.has_perm('products.can_unpublish_product'):
            if 'is_published' in form.fields:
                del form.fields['is_published']
        return form



class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        product = super().get_queryset().get(pk=self.kwargs['pk'])

        if (product.owner == self.request.user or
                self.request.user.has_perm('products.delete_product')):
            return super().get_queryset()
        raise PermissionDenied("У вас нет прав для удаления этого продукта")



class ProductModerationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'products/product_moderation.html'
    fields = ['is_published']
    success_url = reverse_lazy('product_list')

    def test_func(self):

        return self.request.user.has_perm('products.can_unpublish_product')


class ProductDetailView:
    pass


class ProductListView:
    pass