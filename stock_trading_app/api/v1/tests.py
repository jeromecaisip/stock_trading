import pytest
from stock_trading_app.stocks.models import Order
from stock_trading_app.stocks.tests.factories import OrderFactory, StockFactory

pytestmark = pytest.mark.django_db


def test_stocks_buying(trader_api_client, stock):
    trader, api_client = trader_api_client
    json = {
        "transaction_type": Order.BUY,
        "stock": stock.id,
        "num_shares": 10,
        "traded_at": stock.price,
        "trader": trader.id,
    }
    api_path = "/api/v1/orders/"

    response = api_client.post(api_path, data=json, format="json")
    assert response.status_code == 201
    assert trader.orders.filter(stock=stock).exists()
    assert trader.total_bought_price == stock.price * 10


def test_stocks_selling(trader_api_client, stock):
    trader, api_client = trader_api_client
    json = {
        "transaction_type": Order.SELL,
        "stock": stock.id,
        "num_shares": 10,
        "traded_at": stock.price,
        "trader": trader.id,
    }
    api_path = "/api/v1/orders/"

    response = api_client.post(api_path, data=json, format="json")
    assert response.status_code == 201
    assert trader.orders.filter(stock=stock, transaction_type=Order.SELL).exists()
    assert trader.total_sold_price == stock.price * 10


def test_get_total_spent(trader_api_client, stock):
    api_path = "/api/v1/orders/order_value?transaction_type={}".format(Order.BUY)

    trader, api_client = trader_api_client
    order_1, order_2, order_3 = OrderFactory.create_batch(
        3, trader=trader, transaction_type=Order.BUY
    )
    response = api_client.get(api_path, format="json", follow=True)
    assert response.status_code == 200
    assert response.data["total"] == (
        order_1.order_value + order_2.order_value + order_3.order_value
    )

    # Test for single stock
    order_4, order_5 = OrderFactory.create_batch(
        2, trader=trader, stock=stock, transaction_type=Order.BUY
    )
    api_path = "/api/v1/orders/order_value?transaction_type={}&stock={}".format(
        Order.BUY, stock.id
    )
    response = api_client.get(api_path, format="json", follow=True)
    assert response.status_code == 200
    assert response.data["total"] == order_4.order_value + order_5.order_value


def test_multiple_buy_sell(trader_api_client, stock):
    stock_1, stock_2, stock_3 = StockFactory.create_batch(3)
    trader, api_client = trader_api_client
    api_path = "/api/v1/orders/"

    for stock_shares in [(stock_1, 8), (stock_2, 9), (stock_3, 12)]:
        stock, shares = stock_shares
        json = {
            "transaction_type": Order.BUY,
            "stock": stock.id,
            "num_shares": shares,
            "traded_at": stock.price,
            "trader": trader.id,
        }
        response = api_client.post(api_path, data=json, format="json")
        assert response.status_code == 201

    for stock_shares in [(stock_1, 2), (stock_2, 3), (stock_3, 6)]:
        stock, shares = stock_shares
        json = {
            "transaction_type": Order.SELL,
            "stock": stock.id,
            "num_shares": shares,
            "traded_at": stock.price,
            "trader": trader.id,
        }
        response = api_client.post(api_path, data=json, format="json")
        assert response.status_code == 201

    assert trader.current_stock_holdings.get(id=stock_1.id).current_holdings == 8 - 2
    assert trader.current_stock_holdings.get(id=stock_2.id).current_holdings == 9 - 3
    assert trader.current_stock_holdings.get(id=stock_3.id).current_holdings == 12 - 6
