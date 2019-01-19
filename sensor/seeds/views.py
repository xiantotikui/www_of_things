from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseServerError

import json

from .models import Seed

@csrf_exempt
def index(request):
    if request.method == 'POST':
        response = json.loads(request.body.decode('utf8'))
        try:
            Seed.objects.create(device_name=response['name'], device_type=response['type'], device_address=response['address'], device_token=response['token'])
            return HttpResponse()
        except:
            return HttpResponseServerError(500)
