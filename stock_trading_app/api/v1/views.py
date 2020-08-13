from rest_framework import viewsets
from .serializers import OrderSerializer
from stock_trading_app.stocks.models import Order
from rest_framework.decorators import action
from rest_framework.response import Response


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    http_method_names = ["get", "post", "put"]

    def get_queryset(self):
        request = self.request
        trader = request.user.profile
        qs = trader.orders

        if request.query_params.get("transaction_type", "") in [Order.BUY, Order.SELL]:
            transaction_type = request.query_params["transaction_type"]
            qs = qs.filter(transaction_type=transaction_type)

        if request.query_params.get("stock", ""):
            stock_id = request.query_params["stock"]
            qs = qs.filter(stock_id=stock_id)

        return qs

    @action(methods=["GET"], detail=False)
    def order_value(self, request):
        qs = self.get_queryset()
        total = qs.total_order_value()

        return Response(data={"total": total})
