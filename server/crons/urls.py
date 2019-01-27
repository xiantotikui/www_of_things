from django.urls import path
from . import views

app_name = 'crons'

urlpatterns = [
    path('', views.index, name='index'),
    path('/create', views.create, name='create'),
    path('/<str:name>', views.show, name='show'),
    path('/<str:name>/update', views.update, name='update'),
    path('/<str:name>/delete', views.delete, name='delete'),
]
