import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensor.settings')

app = Celery('sensor')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.broker_url = 'redis://[::1]:6379/1'
app.conf.result_backend = 'redis://[::1]:6379/1'
