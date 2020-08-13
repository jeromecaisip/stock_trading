import factory
from factory import fuzzy

from stock_trading_app.stocks.models import Stock, Order
from stock_trading_app.users.tests.factories import ProfileFactory


class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stock

    name = factory.Faker('company')
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    owner = factory.SubFactory(ProfileFactory)
    stock = factory.SubFactory(StockFactory)
    num_shares = factory.Faker('pyint', min_value=1, max_value=10)
    traded_at = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    transaction_type = fuzzy.FuzzyChoice(Order.TRANSACTION_TYPES, getter=lambda c: c[0])
