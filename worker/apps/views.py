import json
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseServerError, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from seeds.models import Seed
from .models import Worker, WorkerState
from .tasks import run_workers

def __check_token(r):
    try:
        return r['token'] == str(Seed.objects.first().device_token)
    except:
        return False

@csrf_exempt
def index(request):
    if request.method == 'POST':
        response = json.loads(request.body.decode('utf8'))
        if __check_token(response):
            try:
                uniq = Worker.objects.values('worker_type').distinct()
            except:
                return HttpResponseServerError(500)
            u = []
            for e in uniq:
                u.append(e['worker_type'])
            available_workers = {'workers': u}
        
            return JsonResponse(available_workers)
        else:
            return HttpResponseForbidden(403)

@csrf_exempt
def worker(request, worker_type):
    if request.method == 'POST':
        response = json.loads(request.body.decode('utf8'))
        if __check_token(response):
            try:
                workers = Worker.objects.filter(worker_type=worker_type)
            except:
                return HttpResponseServerError(500)
            workers_raw = []
            for e in workers:
                workers_raw.append(e.worker_name)
            workers = {'workers': workers_raw}
        
            return JsonResponse(workers)
        else:
            return HttpResponseForbidden(403)

@csrf_exempt
def single_worker(request, worker_type, worker_name):
    if request.method == 'POST':
        response = json.loads(request.body.decode('utf8'))
        if __check_token(response):
            try:
                all_workers = Worker.objects.filter(worker_type=worker_type)
                workers = all_workers.get(worker_name=worker_name)
                values = WorkerState.objects.filter(worker_device=workers)
            except:
                return HttpResponseServerError(500)
            states_raw = []
            for e in values:
                states_raw.append([e.worker_state, e.created_date])
            workers = {'workers': states_raw}

            return JsonResponse(workers)
        else:
            return HttpResponseForbidden(403)

@csrf_exempt
def run_worker(request, worker_type, worker_name):
    if request.method == 'POST':
        response = json.loads(request.body.decode('utf8'))
        if __check_token(response):
            secounds = int(response['time'])
            try:
                all_workers = Worker.objects.filter(worker_type=worker_type)
                workers = all_workers.get(worker_name=worker_name)
                run_workers.delay(worker_name, secounds)
                return HttpResponse(200)
            except:
                return HttpResponseServerError(500)
        else:
            return HttpResponseForbidden(403)