import requests
import json

from pytz import timezone

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from backend.models import Device
from .models import Task

from .forms import TaskForm

def __is_moderator(user):
    return user.groups.filter(name='Mod').exists()

@login_required
def index(request):
    pass

@login_required
@user_passes_test(__is_moderator)
def create(request):
    if request.method == 'GET':
        form = TaskForm()
        return render(request, 'tasks/create.html', {'form': form})
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            __register_task(post.task_name)
    return render(request, 'tasks/index.html')

def __register_task(name):
    task = get_object_or_404(Task, task_name=name)
    array = json.dumps([task.sensors_names,
                        task.workers_names,
                        task.task_min_value,
                        task.task_min_always,
                        task.task_max_value,
                        task.task_max_always,
                        task.task_exe_time,
                       ])
    schedule, created = IntervalSchedule.objects.get_or_create(every=task.task_refresh, period=IntervalSchedule.SECONDS)
    PeriodicTask.objects.create(interval=schedule, name=task.task_name, enabled=True, task='run-task', args=array)
