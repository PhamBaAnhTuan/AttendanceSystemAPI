"""
URL configuration for AttendanceSystemAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
# from face_recog.views import FaceTrainingView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('user/', include('user.urls')),
    path('api/', include('attendance.urls')),
    path('face_recog/', include('face_recog.urls')),
    # path("face-training/", FaceTrainingView.as_view(), name="face-training"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
