import requests
import json
import os
import secrets

from pytz import timezone

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule, CrontabSchedule

from .models import Device, Task, Cron

from .forms import TaskForm, CronForm

def index(request):
    if request.method == 'GET':
        return render(request, 'frontend/index.html', {})
    else:
        return render(request, 'not_found.html', {})

def __is_admin(user):
    return user.groups.filter(name='Admin').exists()

def __is_moderator(user):
    return user.groups.filter(name='Mod').exists()

@login_required
def user_panel(request):
    if request.method == 'GET':
        return render(request, 'frontend/user_panel.html', {})

@login_required
@user_passes_test(__is_moderator)
def moderator_panel(request):
    if request.method == 'GET':
        return render(request, 'frontend/mod_panel.html', {})

@login_required
@user_passes_test(__is_admin)
def admin_panel(request):
    if request.method == 'GET':
        return render(request, 'frontend/admin_panel.html', {})

@login_required
@user_passes_test(__is_admin)
def seed_index(request):
    if request.method == 'GET':
        return render(request, 'frontend/seed/index.html', {})
    elif request.method == 'POST':
        json_data = request.FILES.get('json_data')
        fs = FileSystemStorage()
        filename = fs.save(json_data.name, json_data)
        path = os.path.join(settings.MEDIA_ROOT, filename)
        try:
            accounts = open(path)
            json_accounts = json.load(accounts)
            for key, value in json_accounts['devices'].items():
                token = secrets.token_urlsafe(64)[:63]
                response = __seed_send(value, token)
                if response.status_code == 200:
                    __seed_populate(value, token)
            os.remove(path)
            return render(request, 'status.html', {'code_int': 200, 'code_ext': response.status_code})
        except:
            os.remove(path)
            return render(request, 'status.html', {'code_int': 500, 'code_ext': response.status_code})

def __seed_populate(value, token):
    Device.objects.create(device_name=value['name'], device_type=value['type'], device_address=value['device'], device_token=token)

def __seed_send(value, token):
    client = requests.session()
    serialized = {'name': value['name'], 'type': value['type'], 'address': value['device'], 'token': token}
    req = client.post('{}seeds/'.format(value['device']), json=serialized)
    return req

@login_required
def device(request):
    devices = Device.objects.filter(device_type='sensors')
    return render(request, 'frontend/device/list.html', {'devices': devices})

@login_required
def device_index(request, identyficator):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/'.format(account.device_address), json=data).content.decode('utf8')

    try:
        req_json = json.loads(req)
        available_urls = req_json['sensors']
        return render(request, 'frontend/device/devices_list.html', {'identyficator': identyficator, 'address': account.device_address, 'available_urls': available_urls})
    except:
        return render(request, 'status.html', {'code_int': 500, 'code_ext': req})

@login_required
def device_sensor(request, identyficator, name):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/sensor/{}'.format(account.device_address, name), json=data).content.decode('utf8')
    try:
        req_json = json.loads(req)
        available_urls = req_json['sensors']
        return render(request, 'frontend/device/sensors_list.html', {'identyficator': identyficator, 'address': account.device_address, 'name': name, 'available_urls': available_urls}) 
    except:
        return render(request, 'status.html', {'code_int': 500, 'code_ext': req})

@login_required
def device_single_sensor(request, identyficator, name, value):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/single_sensor/{}/{}'.format(account.device_address, name, value), json=data).content.decode('utf8')

    try:
        req_json = json.loads(req)
        available_values = req_json['sensors']
        return render(request, 'frontend/device/values_list.html', {'identyficator': identyficator, 'address': account.device_address, 'name': name, 'val': value, 'available_values': available_values})
    except:
        return render(request, 'status.html', {'code_int': 500, 'code_ext': req})

@login_required
def worker(request):
    devices = Device.objects.filter(device_type='workers')
    return render(request, 'frontend/worker/list.html', {'devices': devices})

@login_required
def worker_index(request, identyficator):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/'.format(account.device_address), json=data).content.decode('utf8')
    try:
        req_json = json.loads(req)
        available_urls = req_json['workers']
        return render(request, 'frontend/worker/workers_list.html', {'identyficator': identyficator, 'address': account.device_address, 'available_urls': available_urls})
    except:
        return render(request, 'status.html', {'code_int': 500, 'code_ext': req})

@login_required
def worker_element(request, identyficator, name):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/worker/{}'.format(account.device_address, name), json=data).content.decode('utf8')
    try:
        req_json = json.loads(req)
        available_urls = req_json['workers']
        return render(request, 'frontend/worker/elements_list.html', {'identyficator': identyficator, 'address': account.device_address, 'name': name, 'available_urls': available_urls})
    except:
        return render(request, 'status.html', {'code_int': 500, 'code_ext': req})

@login_required
def worker_single_element(request, identyficator, name, value):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/single_worker/{}/{}'.format(account.device_address, name, value), json=data).content.decode('utf8')

    try:
        req_json = json.loads(req)
        available_values = req_json['workers']
        return render(request, 'frontend/worker/states_list.html', {'identyficator': identyficator, 'address': account.device_address, 'name': name, 'val': value, 'available_values': available_values})
    except:
        return render(request, 'status.html', {'code_int': 500, 'code_ext': req})

@login_required
@user_passes_test(__is_moderator)
def worker_run(request, identyficator, name, value):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token,
            'time': 60,
           }

    client = requests.session()
    req = client.post('{}apps/run_worker/{}/{}'.format(account.device_address, value, name), json=data).content.decode('utf8')
    return render(request, 'status.html', {'code_int': 200, 'code_ext': req})

@login_required
@user_passes_test(__is_moderator)
def task_new(request):
    if request.method == 'GET':
        form = TaskForm()
        return render(request, 'frontend/task/task_edit.html', {'form': form})
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            __register_task(post.task_name)
    return render(request, 'frontend/task/index.html', {'code': 'OK'})

def __register_task(name):
    task = get_object_or_404(Task, task_name=name)
    array = json.dumps([task.sensors_names,
                        task.workers_names,
                        task.task_min_value,
                        task.task_min_always,
                        task.task_max_value,
                        task.task_max_always,
                        task.task_exe_time,
                       ])
    schedule, created = IntervalSchedule.objects.get_or_create(every=task.task_refresh, period=IntervalSchedule.SECONDS)
    PeriodicTask.objects.create(interval=schedule, name=task.task_name, enabled=True, task='run-task', args=array)

@login_required
@user_passes_test(__is_moderator)
def cron_new(request):
    if request.method == 'GET':
        form = CronForm()
        return render(request, 'frontend/task/cron_edit.html', {'form': form})
    elif request.method == 'POST':
        form = CronForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            __register_cron(post.task_name)
    return render(request, 'frontend/task/index.html', {'code': 'OK'})

def __register_cron(name):
    task = get_object_or_404(Cron, task_name=name)
    array = json.dumps([task.workers_names,
                        task.task_exe_time,
                       ])
    cron_array = task.task_cron_value.split(' ')
    schedule, created = CrontabSchedule.objects.get_or_create(minute=cron_array[0],
                                                              hour=cron_array[1],
                                                              day_of_week=cron_array[2],
                                                              day_of_month=cron_array[3],
                                                              month_of_year=cron_array[4],
                                                              timezone=pytz.timezone('Europe/Warsaw')
                                                             )                                                           
    PeriodicTask.objects.create(crontab=schedule, name=task.task_name, enabled=True, task='run-cron', args=array)
