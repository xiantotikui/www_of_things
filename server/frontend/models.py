from django.db import models
from django.utils import timezone

class Alert(models.Model):
    address = models.CharField(max_length=64)
    value = models.CharField(max_length=32)
    created_date = models.DateTimeField(default=timezone.now)
