from django.urls import path

from . import views, feed
from .feed import AlertsFeed

urlpatterns = [
    path('', views.index),
    path('panel/user/', views.user_panel, name='user_panel'),
    path('panel/mod/', views.moderator_panel, name='moderator_panel'),
    path('panel/admin/', views.admin_panel, name='admin_panel'),
    path('seed/index/', views.seed_index, name='seed_index'),
    path('device/', views.device, name='device'),
    path('device/<int:identyficator>/', views.device_index, name='device_index'),
    path('device/<int:identyficator>/<str:name>', views.device_sensor, name='device_sensor'),
    path('device/<int:identyficator>/<str:name>/<str:value>', views.device_single_sensor, name='device_single_sensor'),
    path('worker/', views.worker, name='worker'),
    path('worker/<int:identyficator>/', views.worker_index, name='worker_index'),
    path('worker/<int:identyficator>/<str:name>', views.worker_element, name='worker_element'),
    path('worker/<int:identyficator>/<str:name>/<str:value>', views.worker_single_element, name='worker_single_element'),
    path('worker/<int:identyficator>/<str:name>/<str:value>/run', views.worker_run, name='worker_run'),
    path('task/new', views.task_new, name='task_new'),
    path('cron/new', views.cron_new, name='cron_new'),
    path('alerts/get', feed.get),
    path('alerts/feed.json', AlertsFeed.as_view(), name='alerts'),
]
