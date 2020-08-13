from django.db import models
# Create your models here.
from model_utils.models import TimeStampedModel
from stock_trading_app.users.models import Profile
from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, OuterRef, Subquery, When, Case, Value
from django.db.models.functions import Coalesce


class Stock(TimeStampedModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)


class OrderQuerySet(models.QuerySet):
    def total_bought_price(self):
        result = self.filter(transaction_type=Order.BUY).annotate(
            order_value=ExpressionWrapper(F('num_shares') * F('traded_at'),
                                          output_field=models.DecimalField())).aggregate(Sum('order_value'))

        return result['order_value__sum']

    def total_sold_price(self):
        result = self.filter(transaction_type=Order.SELL).annotate(
            order_value=ExpressionWrapper(F('num_shares') * F('traded_at'),
                                          output_field=models.DecimalField())).aggregate(Sum('order_value'))

        return result['order_value__sum']

    def current_holdings(self):
        agg = self.filter(
            stock=OuterRef('id')).values('stock').annotate(
            shares_bought=Coalesce(Sum(
                Case(
                    When(
                        transaction_type=Order.BUY,
                        then=F('num_shares'),
                    ),
                    default=0,
                    output_field=models.IntegerField()
                )
            ),
                Value(0)
            ),
            shares_sold=Coalesce(Sum(
                Case(
                    When(
                        transaction_type=Order.SELL,
                        then=F('num_shares'),
                    ),
                    default=0,
                    output_field=models.IntegerField()
                )
            ),
                Value(0)
            ),
        )

        return Stock.objects.filter(id__in=self.values('stock__id')).annotate(
            shares_bought=Subquery(
                agg.values('shares_bought')[:1],
                output_field=models.IntegerField()
            ),
            shares_sold=Subquery(
                agg.values('shares_sold')[:1],
                output_field=models.IntegerField()
            ),
        ).annotate(current_holdings=F('shares_bought') - F('shares_sold')).distinct()


class Order(TimeStampedModel):
    BUY = 'B'
    SELL = 'S'
    TRANSACTION_TYPES = (
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    )

    owner = models.ForeignKey(Profile, related_name='orders', on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    stock = models.ForeignKey(Stock, related_name='trades', on_delete=models.PROTECT)
    num_shares = models.IntegerField()
    traded_at = models.DecimalField(verbose_name='Current stock price when order was made', max_digits=10,
                                    decimal_places=2)

    objects = OrderQuerySet.as_manager()

    @property
    def order_value(self):
        return self.num_shares * self.traded_at
