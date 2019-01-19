from django.contrib import admin

from .models import Sensor, SensorValue

admin.site.register(Sensor)
admin.site.register(SensorValue)
