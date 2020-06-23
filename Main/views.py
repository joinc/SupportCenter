# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth, User
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import UserProfile


######################################################################################################################


@login_required
def index(request):
    # Главная страница
    profile = UserProfile.objects.filter(user=request.user).first()
    context = {'profile': profile, }
    return render(request, 'index.html', context)


######################################################################################################################


def login(request):
    # Вход пользователя
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            profile = UserProfile.objects.filter(user=user).first()
            if profile:
                if profile.blocked:
                    messages.info(request, 'Выша учетная запись заблокирована, обратитесь к администратору.')
                    return redirect(reverse('login'))
                auth.login(request, user)
                return redirect(request.POST['next'])
            else:
                auth.login(request, user)
                return redirect(reverse('profile_create'))
        else:
            messages.info(request, 'Не правильно введенные данные')
            return redirect(reverse('login'))
    else:
        if request.GET.get('next'):
            return render(request, 'login.html', {'next': request.GET.get('next')})
        else:
            return render(request, 'login.html', {'next': settings.SUCCESS_URL})


######################################################################################################################


def logout(request):
    # Выход пользователя
    auth.logout(request)
    return redirect(reverse('index'))


######################################################################################################################



