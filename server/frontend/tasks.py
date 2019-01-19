import requests
import json 

from django_celery_beat.models import PeriodicTask
from celery import Celery

from .models import Device, Task

from celery import shared_task

@shared_task(name='refresh-db')
def refresh_database():
    PeriodicTask.objects.update(last_run_at=None)

@shared_task(name='run-task')
def run_task(sensors_names, workers_names, task_min_value, task_min_always, task_max_value, task_max_always, task_exe_time):
    variables = sensors_names.split(' ')
    url = variables[0].split('/')
    address = 'https://' + url[2] + '/'
    name = variables[1]
    value = variables[2]

    account = Device.objects.get(device_address=address)
    token = str(account.device_token)
    data = {'token': token
           }

    req = requests.post('{}apps/single_sensor/{}/{}'.format(address, name, value), json=data).content.decode('utf8')

    value_now = json.loads(req)['sensors'][-1][0]

    logic = (float(value_now) >= task_min_value and float(value_now) <= task_max_value) or \
            (task_min_always == True and float(value_now) <= task_max_value) or \
            (float(value_now) >= task_min_value and task_max_always == True) or \
            (task_min_always and task_max_always)
    if logic:
        variables = workers_names.split(' ')
        url = variables[0].split('/')
        address = 'https://' + url[2] + '/'
        value = variables[1]
        name = variables[2]

        account = Device.objects.get(device_address=address)
        token = str(account.device_token)
        data = {'token': token,
                'time': task_exe_time
               }

        client = requests.session()
        req = client.post('{}apps/run_worker/{}/{}'.format(account.device_address, name, value), json=data).content.decode('utf8')

    PeriodicTask.objects.update(last_run_at=None)

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
