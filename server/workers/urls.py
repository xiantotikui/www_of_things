from django.urls import path
from . import views

app_name = 'workers'

urlpatterns = [
    path('', views.index, name='index'),
    path('/<int:identyficator>/', views.show, name='show'),
    path('/<int:identyficator>/<str:name>', views.online_index, name='online-index'),
    path('/<int:identyficator>/<str:name>/<str:value>', views.online_show, name='online-show'),
    path('/<int:identyficator>/<str:name>/<str:value>/run', views.online_run, name='online-run'),
]
