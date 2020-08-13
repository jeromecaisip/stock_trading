import pytest

from stock_trading_app.users.models import User, Profile
from stock_trading_app.stocks.tests.factories import StockFactory, OrderFactory
from stock_trading_app.users.tests.factories import ProfileFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def trader():
    return ProfileFactory.create()


@pytest.fixture()
def stock():
    return StockFactory.create()
