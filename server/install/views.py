import requests
import json
import os
import secrets

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from backend.models import Device

def __is_admin(user):
    return user.groups.filter(name='Admin').exists()

@login_required
@user_passes_test(__is_admin)
def index(request):
    if request.method == 'GET':
        return render(request, 'install/index.html', {})
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
                response = __send(value, token)
                if response.status_code == 200:
                    __populate(value, token)
            os.remove(path)
            return render(request, 'frontend/status.html', {'code_int': 200, 'code_ext': response.status_code})
        except:
            os.remove(path)
            return render(request, 'frontend/status.html', {'code_int': 500, 'code_ext': response.status_code})

def __populate(value, token):
    Device.objects.create(device_name=value['name'], device_type=value['type'], device_address=value['device'], device_token=token)

def __send(value, token):
    client = requests.session()
    serialized = {'name': value['name'], 'type': value['type'], 'address': value['device'], 'token': token}
    req = client.post('{}seeds/'.format(value['device']), json=serialized)
    return req
