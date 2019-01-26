import requests
import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from backend.models import Device

@login_required
def index(request):
    devices = Device.objects.filter(device_type='sensors')
    return render(request, 'sensors/index.html', {'devices': devices})

@login_required
def show(request, identyficator):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/'.format(account.device_address), json=data).content.decode('utf8')

    try:
        req_json = json.loads(req)
        available_urls = req_json['sensors']
        return render(request, 'sensors/show.html', {'identyficator': identyficator, 'address': account.device_address, 'available_urls': available_urls})
    except:
        return render(request, 'frontend/status.html', {'code_int': 500, 'code_ext': req})

@login_required
def online_index(request, identyficator, name):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/sensor/{}'.format(account.device_address, name), json=data).content.decode('utf8')
    try:
        req_json = json.loads(req)
        available_urls = req_json['sensors']
        return render(request, 'sensors/online-index.html', {'identyficator': identyficator, 'address': account.device_address, 'name': name, 'available_urls': available_urls}) 
    except:
        return render(request, 'frontend/status.html', {'code_int': 500, 'code_ext': req})

@login_required
def online_show(request, identyficator, name, value):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/single_sensor/{}/{}'.format(account.device_address, name, value), json=data).content.decode('utf8')

    try:
        req_json = json.loads(req)
        available_values = req_json['sensors']
        return render(request, 'sensors/online-show.html', {'identyficator': identyficator, 'address': account.device_address, 'name': name, 'val': value, 'available_values': available_values})
    except:
        return render(request, 'frontend/status.html', {'code_int': 500, 'code_ext': req})

@login_required
def online_chart(request, identyficator, name, value):
    account = get_object_or_404(Device, id=identyficator)

    token = str(account.device_token)

    data = {'token': token}

    client = requests.session()
    req = client.post('{}apps/single_sensor/{}/{}'.format(account.device_address, name, value), json=data).content.decode('utf8')

    try:
        req_json = json.loads(req)
        available_values = req_json['sensors']
        tmp = []
        for e in available_values:
            tmp.append([e[1], e[0]])
        return render(request, 'sensors/online-chart.html', {'identyficator': identyficator, 'address': account.device_address, 'name': name, 'val': value, 'available_values': tmp})
    except:
        return render(request, 'frontend/status.html', {'code_int': 500, 'code_ext': req})
