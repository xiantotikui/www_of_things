from django.db import models
from django.utils import timezone

class Server(models.Model):
    server_address = models.CharField(max_length=64)
    created_date = models.DateTimeField(default=timezone.now)

class Device(models.Model):
    device_name = models.CharField(max_length=32, unique=True)
    device_type = models.CharField(max_length=32)
    device_address = models.CharField(max_length=64)
    device_token = models.CharField(max_length=64)
    created_date = models.DateTimeField(default=timezone.now)

class Task(models.Model):
    task_name = models.CharField(max_length=32)
    task_refresh = models.IntegerField()
    sensors_names = models.TextField()
    workers_names = models.TextField()
    task_min_value = models.FloatField()
    task_min_always = models.BooleanField()
    task_max_value = models.FloatField()
    task_max_always = models.BooleanField()
    task_exe_time = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

class Cron(models.Model):
    task_name = models.CharField(max_length=32)
    task_refresh = models.IntegerField()
    workers_names = models.TextField()
    task_cron_value = models.CharField(max_length=32)
    task_exe_time = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

class Alert(models.Model):
    address = models.CharField(max_length=64)
    value = models.CharField(max_length=32)
    created_date = models.DateTimeField(default=timezone.now)
