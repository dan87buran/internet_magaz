from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Product


class Command(BaseCommand):
    help = 'Создает группы с правами доступа'

    def handle(self, *args, **options):
        # Получаем контент-тайп для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # 1. Создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(
            name='Модератор продуктов'
        )

        # Права для модератора
        moderator_permissions = [
            'can_unpublish_product',  # Кастомное право
            'delete_product',  # Стандартное право удаления
            'view_product',  # Право просмотра
        ]

        for perm_codename in moderator_permissions:
            try:
                permission = Permission.objects.get(
                    content_type=content_type,
                    codename=perm_codename
                )
                moderator_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Право {perm_codename} не найдено')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Группа "{moderator_group.name}" создана/обновлена')
        )