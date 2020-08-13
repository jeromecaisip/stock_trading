import pytest
from stock_trading_app.stocks.models import Order
from stock_trading_app.stocks.tests.factories import StockFactory, OrderFactory


@pytest.mark.django_db
def test_aggregation_of_total_spent(trader):
    stock_1, stock_2, stock_3 = StockFactory.create_batch(3)

    Order.objects.create(
        owner=trader,
        transaction_type=Order.BUY,
        stock=stock_1,
        num_shares=2,
        traded_at=stock_1.price,
    )
    total = stock_1.price * 2
    assert trader.total_bought_price == total

    Order.objects.create(
        owner=trader,
        transaction_type=Order.BUY,
        stock=stock_2,
        num_shares=5,
        traded_at=stock_2.price,
    )

    assert trader.orders.count() == 2
    total += stock_2.price * 5
    assert trader.total_bought_price == total

    Order.objects.create(
        owner=trader,
        transaction_type=Order.BUY,
        stock=stock_3,
        num_shares=8,
        traded_at=stock_3.price,
    )

    assert trader.orders.count() == 3
    total += stock_3.price * 8
    assert trader.total_bought_price == total


@pytest.mark.django_db
def test_aggregation_of_total_sold(trader):
    stock_1, stock_2, stock_3 = StockFactory.create_batch(3)

    Order.objects.create(
        owner=trader,
        transaction_type=Order.SELL,
        stock=stock_1,
        num_shares=2,
        traded_at=stock_1.price,
    )
    total = stock_1.price * 2
    assert trader.total_sold_price == total

    Order.objects.create(
        owner=trader,
        transaction_type=Order.SELL,
        stock=stock_2,
        num_shares=5,
        traded_at=stock_2.price,
    )

    assert trader.orders.count() == 2
    total += stock_2.price * 5
    assert trader.total_sold_price == total

    Order.objects.create(
        owner=trader,
        transaction_type=Order.SELL,
        stock=stock_3,
        num_shares=8,
        traded_at=stock_3.price,
    )

    assert trader.orders.count() == 3
    total += stock_3.price * 8
    assert trader.total_sold_price == total


@pytest.mark.django_db
def test_current_stock_holdings(trader, stock):
    stock_1, stock_2, stock_3 = StockFactory.create_batch(3)
    Order.objects.create(
        owner=trader,
        transaction_type=Order.BUY,
        stock=stock_1,
        num_shares=5,
        traded_at=stock_1.price,
    )

    Order.objects.create(
        owner=trader,
        transaction_type=Order.SELL,
        stock=stock_1,
        num_shares=3,
        traded_at=stock_1.price,
    )
    assert trader.current_stock_holdings.get(id=stock_1.id).current_holdings == (5 - 3)

    Order.objects.create(
        owner=trader,
        transaction_type=Order.BUY,
        stock=stock_2,
        num_shares=5,
        traded_at=stock_1.price,
    )

    Order.objects.create(
        owner=trader,
        transaction_type=Order.BUY,
        stock=stock_2,
        num_shares=12,
        traded_at=stock_1.price,
    )

    Order.objects.create(
        owner=trader,
        transaction_type=Order.SELL,
        stock=stock_2,
        num_shares=8,
        traded_at=stock_1.price,
    )

    assert trader.current_stock_holdings.get(id=stock_2.id).current_holdings == 5 + 12 - 8
