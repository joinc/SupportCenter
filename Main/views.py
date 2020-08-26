# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse
from Profile.models import UserProfile
from Main.models import Organization
from Esign.classes import EsignCount
from Main.forms import FormOrganization, FormOrganizationList
from Main.tools import get_current_user
from Main.decorators import access_organization_edit


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


@login_required
def organization_list(request):
    current_user = get_current_user(request)
    context = {
        'current_user': current_user,
        'org_list': list(Organization.objects.values('id', 'short_title').all()),
        'form_organization': FormOrganization(),
        'form_organization_list': FormOrganizationList(),
    }
    if request.POST and current_user.access.organization_edit:
        if 'addorg' in request.POST:
            short_title = request.POST['short_title']
            long_title = request.POST['long_title']
            parent_organization = request.POST['parent_organization']
            organization = Organization()
            organization.short_title = short_title
            organization.long_title = long_title
            if parent_organization:
                organization.parent_organization_id = int(parent_organization)
            organization.save()
            return redirect(reverse('organization_list'))
    return render(request, 'organization/list.html', context)


######################################################################################################################


@login_required
def organization_show(request, organization_id):
    context = {
        'current_user': get_current_user(request),
        'organization': get_object_or_404(Organization, id=organization_id),
    }
    return render(request, 'organization/show.html', context)


######################################################################################################################


@access_organization_edit
def organization_delete(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)
    organization.delete()
    return redirect(reverse('organization_list'))


######################################################################################################################


@access_organization_edit
def organization_edit(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)
    context = {
        'current_user': get_current_user(request),
        'organization': organization,
        'form_organization': FormOrganization(instance=organization),
        'form_organization_list': FormOrganizationList(instance=organization),
    }
    return render(request, 'organization/edit.html', context)


######################################################################################################################
