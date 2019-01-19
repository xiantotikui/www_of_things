from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('worker/<str:worker_type>', views.worker),
    path('single_worker/<str:name>/<str:worker_type>', views.single_worker),
    path('run_worker/<str:name>/<str:worker_type>', views.run_worker),
]

