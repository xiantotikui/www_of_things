import requests
import math
import time
from datetime import datetime

from celery import Celery
from celery import shared_task
from django_celery_beat.models import PeriodicTask
from seeds.models import Server, Seed
from .models import Sensor, SensorValue
from .sensors import Sensors

@shared_task(name='refresh-db')
def refresh_database():
    PeriodicTask.objects.update(last_run_at=None)

@shared_task(name='read-sensors')
def read_sensors(name): 
    sensors = Sensor.objects.filter(sensor_name=name)
    for sensor in sensors:
        value = Sensors()
        if sensor.sensor_type == 'DS18B20':
            array = value.DS18B20(sensor.sensor_phys_addr)
            temp = array[0]
            logic = array[1]
            save_value = lambda : SensorValue.objects.create(sensor_device=sensor, sensor_value=str(temp)[0:7])
            if SensorValue.objects.filter(sensor_device=sensor).last() != None:
                result_query = SensorValue.objects.filter(sensor_device=sensor).last()
                last_result = result_query.sensor_value
                if float(last_result) - 0.25 > float(temp) or float(last_result) + 0.25 < float(temp):
                    save_value()
                    time.sleep(0.2)
                    if logic:
                        client = requests.session()
                        req = client.post('{}alerts/get'.format(Server.objects.get(id=1).server_address), json={'alert': {'address': \
                                     (Seed.objects.all().last().device_address + sensor.sensor_type + '/' + sensor.sensor_name), 'value': 'Wartość: {}°C, Data: {}'.format(last_result, datetime.strptime(str(result_query.created_date)[:-13], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))}})
            else:
                save_value()
                time.sleep(0.2)
                result_query = SensorValue.objects.filter(sensor_device=sensor).last()
                last_result = result_query.sensor_value
                if logic:
                    client = requests.session()
                    req = client.post('{}alerts/get'.format(Server.objects.get(id=1).server_address), json={'alert': {'address': \
                                       (Seed.objects.all().last().device_address + sensor.sensor_type + '/' + sensor.sensor_name), 'value': 'Wartość: {}°C, Data: {}'.format(last_result, datetime.strptime(str(result_query.created_date)[:-13], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))}})                
    PeriodicTask.objects.update(last_run_at=None)
