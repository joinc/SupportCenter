# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse
from Profile.models import UserProfile
from Esign.tools import get_esign_count, get_esign_expires_count
from .tools import get_current_user


######################################################################################################################


@login_required
def index(request):
    """
    Отображение главной страницы
    :param request:
    :return:
    """
    current_user = get_current_user(request)
    context = {
        'current_user': current_user,
    }
    if current_user.access.esign_list:
        esign_count_list = get_esign_count(current_user=current_user)
        esign_expires_count = get_esign_expires_count(current_user=current_user)
        context['esign_expires_count'] = esign_expires_count
        context['esign_count_list'] = esign_count_list
    return render(request, 'index.html', context)


######################################################################################################################


def login(request):
    """
    Вход пользователя
    :param request:
    :return:
    """
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
    """
    Выход пользователя
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect(reverse('index'))


######################################################################################################################
