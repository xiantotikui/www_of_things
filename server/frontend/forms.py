from django import forms

from .models import Task, Cron

class TaskForm(forms.ModelForm):

    task_min_value = forms.CharField(required=False)
    task_max_value = forms.CharField(required=False)

    class Meta:
        model = Task
        fields = ('task_name',
                 'task_refresh',
                 'sensors_names',
                 'workers_names',
                 'task_min_value',
                 'task_min_always',
                 'task_max_value',
                 'task_max_always',
                 'task_exe_time',
                )
        labels = {'task_name': 'Nazwa zadania',
                 'task_refresh': 'Częstotliwość odświeżania',
                 'sensors_names': 'Adres czujnika w formacie: [URL typ nazwa]',
                 'workers_names': 'Adres urzadzenia wykonawczego w formacie [URL typ nazwa]',
                 'task_min_value': 'Minimalna wartość graniczna do uruchomienia',
                 'task_min_always': 'Bez dolnej granicy',
                 'task_max_value': 'Maksymalna  wartość graniczna do uruchomienia',
                 'task_max_always': 'Bez górnej granicy',
                 'task_exe_time': 'Czas działania urzadzenia',
                 }

class CronForm(forms.ModelForm):
    class Meta:
        model = Cron
        fields = ('task_name',
                 'task_refresh',
                 'workers_names',
                 'task_cron_value',
                 'task_exe_time',
                )
        labels = {'task_name': 'Nazwa zadania',
                 'task_refresh': 'Częstotliwość odświeżania',
                 'workers_names': 'Adres urzadzenia wykonawczego w formacie [URL typ nazwa]',
                 'task_cron_value': 'Wartość cron',
                 'task_exe_time': 'Czas działania urzadzenia',
                }
