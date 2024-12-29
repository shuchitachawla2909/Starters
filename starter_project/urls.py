
from django.contrib import admin
from django.urls import path,include 

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from userauths import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("rest.urls")),
    path('users/', include("userauths.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)