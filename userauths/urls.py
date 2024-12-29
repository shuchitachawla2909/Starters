from django.urls import path
from userauths import views as user_views

from django.conf import settings
from django.conf.urls.static import static

app_name="userauths"

urlpatterns=[
  path("sign-up/",user_views.register_view,name="sign-up"),
  path("sign-in/",user_views.login_view,name="sign-in"),
  path("sign-out/",user_views.logout_view,name="sign-out"),
  path("profile/",user_views.profile,name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)