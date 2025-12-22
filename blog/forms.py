from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    """Форма для создания и редактирования блоговых записей"""

    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'content', 'preview', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'preview': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'slug': 'Латинские буквы, цифры, дефисы и подчеркивания',
        }

    def clean_slug(self):
        """Валидация slug"""
        slug = self.cleaned_data.get('slug')
        if not slug.replace('-', '').replace('_', '').isalnum():
            raise forms.ValidationError('Slug может содержать только латинские буквы, цифры, дефисы и подчеркивания')
        return slug