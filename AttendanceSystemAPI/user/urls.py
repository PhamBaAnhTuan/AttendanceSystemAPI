from django.urls import path, include
from user.views import UserViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
# router = SimpleRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = router.urls