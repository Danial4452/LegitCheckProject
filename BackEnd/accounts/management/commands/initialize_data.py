from django.core.management.base import BaseCommand
from LegitCheckProject.BackEnd.accounts.models import Role
from LegitCheckProject.BackEnd.orders.models import OrderStatus


class Command(BaseCommand):
    help = 'Initialize roles and order statuses'

    def handle(self, *args, **options):
        # Create roles
        roles_data = [
            ('client', 'Клиент'),
            ('courier', 'Курьер'),
            ('support', 'Поддержка'),
        ]

        for name, description in roles_data:
            role, created = Role.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Создана роль: {name}')
                )
            else:
                self.stdout.write(f'✓ Роль существует: {name}')

        # Create order statuses
        statuses_data = ['new', 'accepted', 'in_delivery', 'delivered', 'cancelled']

        for status_name in statuses_data:
            status, created = OrderStatus.objects.get_or_create(name=status_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Создан статус: {status_name}')
                )
            else:
                self.stdout.write(f'✓ Статус существует: {status_name}')

        self.stdout.write(
            self.style.SUCCESS('\nДанные инициализированы успешно!')
        )
