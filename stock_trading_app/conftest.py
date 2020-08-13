import pytest

from stock_trading_app.users.models import User, Profile
from stock_trading_app.stocks.tests.factories import StockFactory, OrderFactory, Order
from stock_trading_app.users.tests.factories import ProfileFactory
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def trader():
    return ProfileFactory.create()


@pytest.fixture
def stock():
    return StockFactory.create()


@pytest.fixture
def bought_order():
    return OrderFactory.create(transaction_type=Order.BUY)


@pytest.fixture
def sold_order():
    return OrderFactory.create(transaction_type=Order.SELL)


@pytest.fixture
def trader_api_client(trader):
    user = trader.user
    client = APIClient()
    client.force_authenticate(user=user)
    return trader, client


@pytest.fixture
def anonymous_api_client():
    return APIClient()
