from django import forms

from django.utils.translation import ugettext_lazy as _

from .models import Cron

class CronForm(forms.ModelForm):
    class Meta:
        model = Cron
        fields = ('task_name',
                 'task_refresh',
                 'workers_names',
                 'task_cron_value',
                 'task_exe_time',
                )
        labels = {'task_name': _('CronFormName'),
                 'task_refresh': _('CronFormRefresh'),
                 'workers_names': _('CronFormWrkNames'),
                 'task_cron_value': _('CronFormCronVal'),
                 'task_exe_time': _('CronFormExe'),
                }
