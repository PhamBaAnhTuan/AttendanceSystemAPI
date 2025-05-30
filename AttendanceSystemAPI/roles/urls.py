from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import RoleViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'', RoleViewSet, basename='role')

urlpatterns = router.urls