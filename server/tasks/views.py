import requests
import json

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
    return render(request, 'tasks/index.html', {'data': Task.objects.all()})

@login_required
def show(request, name):
    return render(request, 'tasks/show.html', {'data': get_object_or_404(Task, task_name=name)})

@login_required
@user_passes_test(__is_moderator)
def create(request):
    if request.method == 'GET':
        form = TaskForm()
        return render(request, 'tasks/form.html', {'form': form})
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            __create(post.task_name)
    return render(request, 'tasks/index.html', {'data': Task.objects.all()})

def __create(name):
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

@login_required
@user_passes_test(__is_moderator)
def update(request, name):
    task = get_object_or_404(Task, task_name=name)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'tasks/form.html', {'form': form})
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            __update(post.task_name)
    return render(request, 'tasks/index.html', {'data': Task.objects.all()})

def __update(name):
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
    PeriodicTask.objects.get(name=name).delete()
    PeriodicTask.objects.create(interval=schedule, name=task.task_name, enabled=True, task='run-task', args=array)

@login_required
@user_passes_test(__is_moderator)
def delete(request, name):
    task = get_object_or_404(Task, task_name=name)
    if request.method == 'GET':
        return render(request, 'tasks/delete.html', {'task': task.task_name})
    elif request.method == 'POST':
        try:
            __delete(task.task_name)
        except:
            pass
        task.delete()
        return render(request, 'tasks/index.html', {'data': Task.objects.all()})

def __delete(name):
    task = get_object_or_404(Task, task_name=name)
    PeriodicTask.objects.get(name=name).delete()