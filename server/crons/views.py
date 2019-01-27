import requests
import json

from pytz import timezone

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from django_celery_beat.models import PeriodicTask, CrontabSchedule

from backend.models import Device
from .models import Cron

from .forms import CronForm

def __is_moderator(user):
    return user.groups.filter(name='Mod').exists()

@login_required
def index(request):
    return render(request, 'crons/index.html', {'data': Cron.objects.all()})

@login_required
def show(request, name):
    return render(request, 'crons/show.html', {'data': get_object_or_404(Cron, task_name=name)})

@login_required
@user_passes_test(__is_moderator)
def create(request):
    if request.method == 'GET':
        form = CronForm()
        return render(request, 'crons/form.html', {'form': form})
    elif request.method == 'POST':
        form = CronForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            __create(post.task_name)
    return render(request, 'crons/index.html', {'data': Cron.objects.all()})

def __create(name):
    task = get_object_or_404(Cron, task_name=name)
    array = json.dumps([task.workers_names,
                        task.task_exe_time,
                       ])
    cron_array = task.task_cron_value.split(' ')
    schedule, created = CrontabSchedule.objects.get_or_create(minute=cron_array[0],
                                                              hour=cron_array[1],
                                                              day_of_week=cron_array[2],
                                                              day_of_month=cron_array[3],
                                                              month_of_year=cron_array[4],
                                                              timezone=timezone('Europe/Warsaw')
                                                             )                                                           
    PeriodicTask.objects.create(crontab=schedule, name=task.task_name, enabled=True, task='run-cron', args=array)

@login_required
@user_passes_test(__is_moderator)
def update(request, name):
    task = get_object_or_404(Cron, task_name=name)
    if request.method == 'GET':
        form = CronForm(instance=task)
        return render(request, 'crons/form.html', {'form': form})
    elif request.method == 'POST':
        form = CronForm(request.POST, instance=task)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            __update(post.task_name)
    return render(request, 'crons/index.html', {'data': Cron.objects.all()})

def __update(name):
    task = get_object_or_404(Cron, task_name=name)
    array = json.dumps([task.workers_names,
                        task.task_exe_time,
                       ])
    cron_array = task.task_cron_value.split(' ')
    schedule, created = CrontabSchedule.objects.get_or_create(minute=cron_array[0],
                                                              hour=cron_array[1],
                                                              day_of_week=cron_array[2],
                                                              day_of_month=cron_array[3],
                                                              month_of_year=cron_array[4],
                                                              timezone=timezone('Europe/Warsaw')
                                                             )
    PeriodicTask.objects.get(name=name).delete()
    PeriodicTask.objects.create(crontab=schedule, name=task.task_name, enabled=True, task='run-cron', args=array)

@login_required
@user_passes_test(__is_moderator)
def delete(request, name):
    task = get_object_or_404(Cron, task_name=name)
    if request.method == 'GET':
        return render(request, 'crons/delete.html', {'task': task.task_name})
    elif request.method == 'POST':
        try:
            __delete(task.task_name)
        except:
            pass
        task.delete()
        return render(request, 'crons/index.html', {'data': Cron.objects.all()})

def __delete(name):
    task = get_object_or_404(Cron, task_name=name)
    PeriodicTask.objects.get(name=name).delete()
