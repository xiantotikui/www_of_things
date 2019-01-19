from django.db import models
from django.utils import timezone

class Sensor(models.Model):
    sensor_name = models.CharField(max_length=32, unique=True)
    sensor_type = models.CharField(max_length=32)
    sensor_phys_addr = models.CharField(max_length=128)
    created_date = models.DateTimeField(default=timezone.now)

class SensorValue(models.Model):
    sensor_device = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    sensor_value = models.CharField(max_length=8)
    created_date = models.DateTimeField(default=timezone.now)
