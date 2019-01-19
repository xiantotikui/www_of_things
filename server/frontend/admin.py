from django.contrib import admin

from .models import Server, Device, Task, Cron, Alert

admin.site.register(Server)
admin.site.register(Device)
admin.site.register(Task)
admin.site.register(Cron)
admin.site.register(Alert)
