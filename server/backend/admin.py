from django.contrib import admin

from .models import Server, Device

admin.site.register(Server)
admin.site.register(Device)
