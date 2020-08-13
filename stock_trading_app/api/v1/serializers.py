from rest_framework import serializers
from stock_trading_app.stocks.models import Stock, Order
from rest_framework.exceptions import PermissionDenied


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("id", "name", "price")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "trader",
            "transaction_type",
            "stock",
            "num_shares",
            "traded_at",
        )

    def validate_trader(self, value):
        try:
            request = self.context["request"]
            profile = request.user.profile
            if profile != value:
                raise PermissionDenied
            return value
        except KeyError:
            return value
