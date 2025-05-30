from django.urls import re_path
from djangochannelsrestframework.consumers import view_as_consumer
from .views import UserViewSet

websocket_urlpatterns = [
   re_path(r"^user/$", view_as_consumer(UserViewSet.as_view()))
]