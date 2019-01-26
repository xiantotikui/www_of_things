from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('worker/<str:worker_type>', views.worker),
    path('single_worker/<str:worker_type>/<str:worker_name>', views.single_worker),
    path('run_worker/<str:worker_type>/<str:worker_name>', views.run_worker),
]

