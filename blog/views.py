from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import BlogPost
from .forms import BlogPostForm


# Список блоговых записей
class BlogPostListView(ListView):
    """Список опубликованных блоговых записей"""
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blogposts'
    paginate_by = 6

    def get_queryset(self):
        """Получаем только опубликованные записи"""
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


# Детальная страница блоговой записи
class BlogPostDetailView(DetailView):
    """Детальная страница блоговой записи"""
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blogpost'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        """Увеличиваем счетчик просмотров при открытии статьи"""
        obj = super().get_object(queryset=queryset)
        obj.views_count = F('views_count') + 1
        obj.save()
        obj.refresh_from_db()  # Обновляем объект из базы данных
        return obj


# Создание блоговой записи
class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание новой блоговой записи"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:blogpost_list')
    permission_required = 'blog.can_publish'

    def form_valid(self, form):
        """Дополнительная обработка при успешном создании"""
        form.instance.author = self.request.user
        return super().form_valid(form)


# Редактирование блоговой записи
class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование блоговой записи"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    permission_required = 'blog.can_publish'

    def get_success_url(self):
        """После успешного редактирования переходим на страницу статьи"""
        return reverse_lazy('blog:blogpost_detail', kwargs={'slug': self.object.slug})


# Удаление блоговой записи
class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление блоговой записи"""
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:blogpost_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    permission_required = 'blog.can_publish'