from django.db import models
from django.utils import timezone

class Worker(models.Model):
    worker_name = models.CharField(max_length=32, unique=True)
    worker_type = models.CharField(max_length=32)
    worker_manual = models.BooleanField()
    created_date = models.DateTimeField(default=timezone.now)

class WorkerState(models.Model):
    worker_device = models.ForeignKey(Worker, on_delete=models.CASCADE)
    worker_state = models.CharField(max_length=8)
    created_date = models.DateTimeField(default=timezone.now)
