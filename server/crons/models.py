from django.db import models
from django.utils import timezone

class Cron(models.Model):
    task_name = models.CharField(max_length=32, unique=True)
    task_refresh = models.IntegerField()
    workers_names = models.TextField()
    task_cron_value = models.CharField(max_length=32)
    task_exe_time = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
