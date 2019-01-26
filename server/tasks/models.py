from django.db import models
from django.utils import timezone

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
