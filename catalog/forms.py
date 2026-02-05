from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category

# Список запрещенных слов
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта с валидацией"""

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Подробное описание товара...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        """Инициализация формы с добавлением стилей Bootstrap"""
        super().__init__(*args, **kwargs)

        # Добавляем классы Bootstrap для всех полей
        for field_name, field in self.fields.items():
            if field_name != 'is_published':  # чекбокс обрабатываем отдельно
                field.widget.attrs['class'] = 'form-control'

            # Добавляем placeholder для текстовых полей
            if field_name in ['name', 'description']:
                field.widget.attrs['placeholder'] = field.label

        # Специальная настройка для поля is_published
        self.fields['is_published'].label = 'Опубликовать товар'
        self.fields['is_published'].help_text = 'Товар будет виден покупателям'

        # Настройка выпадающего списка категорий
        self.fields['category'].empty_label = '-- Выберите категорию --'

    def clean_name(self):
        """Валидация поля name на запрещенные слова"""
        name = self.cleaned_data.get('name', '')

        # Проверка на наличие запрещенных слов (регистронезависимо)
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise ValidationError(
                    f'Название содержит запрещенное слово: "{word}"',
                    code='forbidden_word'
                )

        # Проверка длины названия
        if len(name) < 3:
            raise ValidationError(
                'Название должно содержать минимум 3 символа',
                code='name_too_short'
            )

        return name

    def clean_description(self):
        """Валидация поля description на запрещенные слова"""
        description = self.cleaned_data.get('description', '')

        # Проверка на наличие запрещенных слов (регистронезависимо)
        for word in FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise ValidationError(
                    f'Описание содержит запрещенное слово: "{word}"',
                    code='forbidden_word'
                )

        # Проверка длины описания
        if description and len(description) < 10:
            raise ValidationError(
                'Описание должно содержать минимум 10 символов',
                code='description_too_short'
            )

        return description

    def clean_price(self):
        """Валидация поля price (цена не может быть отрицательной)"""
        price = self.cleaned_data.get('price')

        if price is not None:
            if price < 0:
                raise ValidationError(
                    'Цена не может быть отрицательной',
                    code='negative_price'
                )

            if price > 100000000:  # 100 миллионов
                raise ValidationError(
                    'Цена слишком высокая',
                    code='price_too_high'
                )

        return price

    def clean(self):
        """Общая валидация формы"""
        cleaned_data = super().clean()

        # Дополнительная проверка: цена должна быть указана для опубликованных товаров
        is_published = cleaned_data.get('is_published')
        price = cleaned_data.get('price')

        if is_published and price is None:
            raise ValidationError({
                'price': 'Для опубликованных товаров необходимо указать цену'
            })

        return cleaned_data