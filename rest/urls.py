from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name="rest"


urlpatterns = [
    path('', views.home,name="home"),
    
    path('restaurants/', views.restaurants,name="restaurants"),
    path('add_restaurant/', views.add_restaurant, name='add_restaurant'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/<int:review_id>/update/', views.update_review, name='update_review'),
    path('restaurant/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('tag/<str:tag_name>/', views.restaurants_by_tag, name='restaurants_by_tag'),
    path('add_tag/', views.add_tag, name='add_tag'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)