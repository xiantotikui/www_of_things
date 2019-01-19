from django.contrib import admin

from .models import Worker, WorkerState

admin.site.register(Worker)
admin.site.register(WorkerState)
