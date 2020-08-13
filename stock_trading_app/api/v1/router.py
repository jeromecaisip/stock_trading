from .views import OrderViewSet
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import OrderViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("orders", OrderViewSet)

api_urlpatterns = router.urls
