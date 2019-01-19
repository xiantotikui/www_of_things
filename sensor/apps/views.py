import json
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseServerError, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from seeds.models import Seed
from .models import Sensor, SensorValue

def __check_token(r):
    try:
        return r['token'] == str(Seed.objects.first().device_token)
    except:
        return False

@csrf_exempt
def index(request):
    if request.method == 'POST':
        response = json.loads(request.body.decode('utf8'))
        if __check_token(response):
            try:
                uniq = Sensor.objects.values('sensor_type').distinct()
            except:
                return HttpResponseServerError(500)
            u = []
            for e in uniq:
                u.append(e['sensor_type'])
            available_sensors = {'sensors': u}
        
            return JsonResponse(available_sensors)
        else:
            return HttpResponseForbidden(403)

@csrf_exempt
def sensor(request, sensor_type):
    if request.method == 'POST':
        response = json.loads(request.body.decode('utf8'))
        if __check_token(response):
            try:
                sensors = Sensor.objects.filter(sensor_type=sensor_type)
            except:
                return HttpResponseServerError(500)
            sensors_raw = []
            for e in sensors:
                sensors_raw.append(e.sensor_name)
            sensors = {'sensors': sensors_raw}
        
            return JsonResponse(sensors)
        else:
            return HttpResponseForbidden(403)

@csrf_exempt
def single_sensor(request, sensor_type, sensor_name):
    if request.method == 'POST':
        response = json.loads(request.body.decode('utf8'))
        if __check_token(response):
            try:
                all_sensors = Sensor.objects.filter(sensor_type=sensor_type)
                sensors = all_sensors.get(sensor_name=sensor_name)
                values = SensorValue.objects.filter(sensor_device=sensors)
            except:
                return HttpResponseServerError(500)
            values_raw = []
            for e in values:
                values_raw.append([e.sensor_value, e.created_date])
            sensors = {'sensors': values_raw}

            return JsonResponse(sensors)
        else:
            return HttpResponseForbidden(403)
