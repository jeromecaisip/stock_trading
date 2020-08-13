from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.db import models
from model_utils.models import TimeStampedModel


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True)
    username = models.CharField(
        null=True, blank=True, max_length=100,
    )  # not to be used

    def __str__(self):
        return self.email


class Profile(TimeStampedModel):
    TRADER = "trader"
    PROFILE_TYPES = ((TRADER, "Trader"),)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=PROFILE_TYPES)

    def __str__(self):
        return self.user.email

    @property
    def current_stock_holdings(self):
        return self.orders.current_holdings()

    @property
    def total_bought_price(self):
        return self.orders.total_bought_price()

    @property
    def total_sold_price(self):
        return self.orders.total_sold_price()
