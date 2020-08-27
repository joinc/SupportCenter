# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse
from Profile.models import UserProfile
from Esign.classes import EsignCount
from Main.tools import get_current_user


######################################################################################################################


@login_required
def index(request):
    # Главная страница
    current_user = get_current_user(request)
    esign_count = EsignCount(current_user)
    context = {
        'current_user': current_user,
        'esign_count_current': esign_count.get_current_count(),
        'esign_count_expires': esign_count.get_expires_count(),
        'esign_count_expired': esign_count.get_expired_count(),
        'esign_count_extended': esign_count.get_extended_count(),
        'esign_count_terminate': esign_count.get_terminate_count(),
    }
    return render(request, 'index.html', context)


######################################################################################################################


def login(request):
    # Вход пользователя
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            profile = get_object_or_404(UserProfile, user=user)
            if profile.blocked:
                messages.info(request, 'Выша учетная запись заблокирована, обратитесь к администратору.')
                return redirect(reverse('login'))
            auth.login(request, user)
            return redirect(request.POST['next'])
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
