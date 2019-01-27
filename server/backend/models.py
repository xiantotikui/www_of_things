from django.db import models
from django.utils import timezone

class Server(models.Model):
    server_address = models.CharField(max_length=64, unique=True)
    created_date = models.DateTimeField(default=timezone.now)

class Device(models.Model):
    device_name = models.CharField(max_length=32, unique=True)
    device_type = models.CharField(max_length=32)
    device_address = models.CharField(max_length=64)
    device_token = models.CharField(max_length=64)
    created_date = models.DateTimeField(default=timezone.now)
