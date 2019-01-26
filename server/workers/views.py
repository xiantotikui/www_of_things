import requests
import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from backend.models import Device

def __is_moderator(user):
    return user.groups.filter(name='Mod').exists()

@login_required
def index(request):
    devices = Device.objects.filter(device_type='workers')
    return render(request, 'worker/index.html', {'devices': devices})

@login_required
def show(request, identyficator):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/'.format(account.device_address), json=data).content.decode('utf8')
    try:
        req_json = json.loads(req)
        available_urls = req_json['workers']
        return render(request, 'worker/show.html', {'identyficator': identyficator, 'address': account.device_address, 'available_urls': available_urls})
    except:
        return render(request, 'frontend/status.html', {'code_int': 500, 'code_ext': req})

@login_required
def online_index(request, identyficator, name):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/worker/{}'.format(account.device_address, name), json=data).content.decode('utf8')
    try:
        req_json = json.loads(req)
        available_urls = req_json['workers']
        return render(request, 'worker/online-index.html', {'identyficator': identyficator, 'address': account.device_address, 'name': name, 'available_urls': available_urls})
    except:
        return render(request, 'frontend/status.html', {'code_int': 500, 'code_ext': req})

@login_required
def online_show(request, identyficator, name, value):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/single_worker/{}/{}'.format(account.device_address, name, value), json=data).content.decode('utf8')
    
    try:
        req_json = json.loads(req)
        available_values = req_json['workers']
        
        return render(request, 'worker/online-show.html', {'identyficator': identyficator, 'address': account.device_address, 'name': name, 'val': value, 'available_values': available_values})
    except:
        return render(request, 'frontend/status.html', {'code_int': 500, 'code_ext': req})

@login_required
@user_passes_test(__is_moderator)
def online_run(request, identyficator, name, value):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token,
            'time': 60,
           }

    client = requests.session()
    req = client.post('{}apps/run_worker/{}/{}'.format(account.device_address, name, name), json=data).content.decode('utf8')
    return render(request, 'frontend/status.html', {'code_int': 200, 'code_ext': req})
