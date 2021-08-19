# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from Main.tools import get_profile
from Signature.tools import get_count_signature, get_count_expires_signature

######################################################################################################################


@login_required
def index(request):
    """
    Отображение главной страницы
    :param request:
    :return: HttpResponse
    """
    current_user = get_profile(user=request.user)
    context = {
        'current_user': current_user,
        'title': 'Главная',
    }
    if current_user.access(list_permission=['signature_list', ]):
        context['count_signature'] = get_count_signature(current_user=current_user)
        context['count_expires_signature'] = get_count_expires_signature(current_user=current_user)
    return render(request=request, template_name='index.html', context=context)


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
            profile = get_profile(user=user)
            if profile.blocked:
                messages.warning(request, 'Выша учетная запись заблокирована, обратитесь к администратору.')
                return redirect(reverse('login'))
            auth.login(request, user)
            return redirect(request.POST['next'])
        else:
            messages.error(request, 'Не правильно введенные данные')
            return redirect(reverse('login'))
    else:
        context = {
            'title': 'Авторизация',
        }
        if request.GET.get('next'):
            context['next'] = request.GET.get('next')
        else:
            context['next'] = settings.SUCCESS_URL
        return render(request=request, template_name='login.html', context=context)


######################################################################################################################


def logout(request):
    """
    Выход пользователя
    :param request:
    :return: redirect
    """
    auth.logout(request)
    return redirect(reverse('login'))


######################################################################################################################
