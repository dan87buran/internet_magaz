from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    """Модель блоговой записи"""
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Введите заголовок статьи (максимум 200 символов)'
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL',
        help_text='Введите уникальный URL для статьи (латинские буквы, цифры, дефисы)'
    )

    content = models.TextField(
        verbose_name='Содержимое',
        help_text='Введите текст статьи'
    )

    preview = models.ImageField(
        upload_to='blog/previews/',
        verbose_name='Превью',
        blank=True,
        null=True,
        help_text='Загрузите изображение для превью статьи'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано',
        help_text='Отметьте для публикации статьи'
    )

    views_count = models.IntegerField(
        default=0,
        verbose_name='Количество просмотров',
        editable=False
    )

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'
        ordering = ['-created_at']
        permissions = [
            ('can_publish', 'Может публиковать статьи'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Получение абсолютного URL для записи"""
        return reverse('blog:blogpost_detail', kwargs={'slug': self.slug})

    def increase_views(self):
        """Увеличение счетчика просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])