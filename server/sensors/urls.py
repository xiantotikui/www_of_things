from django.urls import path
from . import views

app_name = 'sensors'

urlpatterns = [
    path('', views.index, name='index'),
    path('/<int:identyficator>/', views.show, name='show'),
    path('/<int:identyficator>/<str:name>', views.online_index, name='online-index'),
    path('/<int:identyficator>/<str:name>/<str:value>', views.online_show, name='online-show'),
	path('/<int:identyficator>/<str:name>/<str:value>/chart', views.online_chart, name='online-chart'),
]
