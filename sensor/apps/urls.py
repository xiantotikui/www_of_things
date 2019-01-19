from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('sensor/<str:sensor_type>', views.sensor),
    path('single_sensor/<str:sensor_type>/<str:sensor_name>', views.single_sensor),
]
