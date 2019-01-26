import requests
import json 

from django_celery_beat.models import PeriodicTask
from celery import Celery

from backend.models import Device
from .models import Cron

from celery import shared_task

@shared_task(name='run-cron')
def run_cron(sensors_names, workers_names, task_exe_time):
    variables = workers_names.split(' ')
    url = variables[0].split('/')
    address = 'https://' + url[2] + '/'
    name = variables[1]
    value = variables[2]
    account = Device.objects.get(device_address=address)
    token = str(account.device_token)
    data = {'token': token,
            'time': task_exe_time
           }
    client = requests.session()
    req = client.post('{}apps/run_worker/{}/{}'.format(account.device_address, name, value), json=data).content.decode('utf8')

    PeriodicTask.objects.update(last_run_at=None)
