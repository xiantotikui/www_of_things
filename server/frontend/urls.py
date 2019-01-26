from django.urls import path
from . import views, feed
from .feed import AlertsFeed

urlpatterns = [
    path('', views.index, name='frontend'),
    path('users', views.user_panel, name='frontend-user'),
    path('mods', views.moderator_panel, name='frontend-mod'),
    path('admins', views.admin_panel, name='frontend-admin'),
    path('alerts/get', feed.get, name='frontend-get'),
    path('alerts/feed.json', AlertsFeed.as_view(), name='frontend-alerts'),
]
