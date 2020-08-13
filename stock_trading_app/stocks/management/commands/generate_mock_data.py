from django.core.management.base import BaseCommand
from stock_trading_app.users.tests.factories import User, ProfileFactory
from stock_trading_app.stocks.tests.factories import StockFactory, OrderFactory


class Command(BaseCommand):
    help = "Generate Mock Data."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(email="test@example.com")
        if created:
            user.set_password("test")
            user.save()

        profile = ProfileFactory.create(user=user)

        orders = OrderFactory.create_batch(10, trader=profile)
        for order in orders:
            self.stdout.write(self.style.SUCCESS(order))

        self.stdout.write(self.style.SUCCESS("Mock data generated!"))

        self.stdout.write(
            self.style.SUCCESS("Login is test@example.com and password is test.")
        )
