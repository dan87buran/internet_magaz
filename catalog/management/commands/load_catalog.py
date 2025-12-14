import json
import os
from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Загрузка тестовых данных для каталога из фикстур'

    def handle(self, *args, **options):
        self.stdout.write("Начало загрузки тестовых данных...")

        # Удаление старых данных
        self.stdout.write("Удаление старых данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Путь к фикстурам
        fixture_path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..', 'fixtures', 'catalog_data.json'
        )

        # Загрузка фикстур
        if os.path.exists(fixture_path):
            self.stdout.write(f"Загрузка данных из {fixture_path}")
            try:
                call_command('loaddata', 'catalog_data.json')
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Успешно загружено: '
                        f'{Category.objects.count()} категорий и '
                        f'{Product.objects.count()} продуктов'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка при загрузке фикстур: {e}')
                )
                # Создание тестовых данных вручную
                self.create_test_data()
        else:
            self.stdout.write(
                self.style.WARNING('Файл фикстур не найден. Создание тестовых данных...')
            )
            self.create_test_data()

    def create_test_data(self):
        """Создание тестовых данных, если фикстуры не найдены"""
        # Создание категорий
        electronics = Category.objects.create(
            name='Электроника',
            description='Техника и гаджеты'
        )
        books = Category.objects.create(
            name='Книги',
            description='Художественная литература'
        )

        # Создание продуктов
        Product.objects.create(
            name='Смартфон',
            description='Современный смартфон',
            category=electronics,
            price=29999.99
        )

        Product.objects.create(
            name='Ноутбук',
            description='Мощный ноутбук для работы',
            category=electronics,
            price=89999.99
        )

        Product.objects.create(
            name='Книга по программированию',
            description='Учебник по Python',
            category=books,
            price=1999.99
        )

        self.stdout.write(
            self.style.SUCCESS('Созданы тестовые данные: 2 категории, 3 продукта')
        )