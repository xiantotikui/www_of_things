from django_celery_beat.models import PeriodicTask
from celery import Celery

from .models import Worker
from .models import WorkerState

from .workers import Workers

from celery import shared_task

@shared_task(name='refresh-db')
def refresh_database():
    PeriodicTask.objects.update(last_run_at=None)

@shared_task(name='run-workers')
def run_workers(name, secounds): 
    w = Workers(name, secounds)
    w.worker()
