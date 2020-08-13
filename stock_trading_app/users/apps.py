from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "stock_trading_app.users"
    verbose_name = _("Users")
