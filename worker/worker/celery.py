import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worker.settings')

app = Celery('worker')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.broker_url = 'redis://localhost:6379/2'
app.conf.result_backend = 'redis://localhost:6379/2'
