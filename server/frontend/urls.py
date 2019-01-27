from django.urls import path
from . import views, feed
from .feed import AlertsFeed

app_name = 'frontend'

urlpatterns = [
    path('', views.index, name='index'),
    path('users', views.user_panel, name='users'),
    path('mods', views.moderator_panel, name='mods'),
    path('admins', views.admin_panel, name='admins'),
    path('alerts/get', feed.get, name='get'),
    path('alerts/feed.json', AlertsFeed.as_view(), name='alerts'),
]
