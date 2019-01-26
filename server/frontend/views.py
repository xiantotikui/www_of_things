from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from backend.models import Server, Device

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})

def __is_admin(user):
    return user.groups.filter(name='Admin').exists()

def __is_moderator(user):
    return user.groups.filter(name='Mod').exists()

@login_required
def user_panel(request):
    if request.method == 'GET':
        return render(request, 'panels/user_panel.html', {})

@login_required
@user_passes_test(__is_moderator)
def moderator_panel(request):
    if request.method == 'GET':
        return render(request, 'panels/mod_panel.html', {})

@login_required
@user_passes_test(__is_admin)
def admin_panel(request):
    if request.method == 'GET':
        return render(request, 'panels/admin_panel.html', {})
