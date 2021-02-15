# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse
from Profile.models import UserProfile
from Signature.tools import get_count_signature, get_count_expires_signature
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
        'title': 'Главная',
    }
    if current_user.access.signature_list:
        context['count_signature'] = get_count_signature(current_user=current_user)
        context['count_expires_signature'] = get_count_expires_signature(current_user=current_user)
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
