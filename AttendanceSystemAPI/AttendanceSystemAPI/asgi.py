"""
ASGI config for AttendanceSystemAPI project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AttendanceSystemAPI.settings')
# application = get_asgi_application()

import django
django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from user import routing
from . import settings

application = ProtocolTypeRouter({
   "http": get_asgi_application(),
   "websocket": AuthMiddlewareStack(
      URLRouter(
         routing.websocket_urlpatterns
      )
   ),
})