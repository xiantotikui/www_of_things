from django import forms

from django.utils.translation import ugettext_lazy as _

from .models import Task

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
        labels = {'task_name': _('TaskFormName'),
                 'task_refresh': _('TaskFormRefresh'),
                 'sensors_names': _('TaskFormSensNames'),
                 'workers_names': _('TaskFormWrkNames'),
                 'task_min_value': _('TaskFormMinVal'),
                 'task_min_always': _('TaskFormMinAllways'),
                 'task_max_value': _('TaskFormMaxVal'),
                 'task_max_always': _('TaskFormMaxAlways'),
                 'task_exe_time': _('TaskFormExe'),
                 }
