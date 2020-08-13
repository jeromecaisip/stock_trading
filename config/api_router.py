from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from stock_trading_app.users.api.views import UserViewSet
from stock_trading_app.api.v1.router import api_urlpatterns as api_v1
from django.urls import path, include

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

app_name = "api"
urlpatterns = router.urls

# Apply versioning on API for the stocks related models only
urlpatterns += [
    path("v1/", include(api_v1)),
]
