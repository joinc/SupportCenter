# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Profile.models import UserProfile, AccessRole
from Profile.tools import get_list_profile, check_password
from Profile.forms import FormChangePassword, FormSearchUser, FormAccessList, FormOrganization, FormCreateUser, \
    FormEditUser, FormAccessRole
from Main.decorators import access_user_edit, access_user_list
from Main.tools import get_current_user
from Organization.models import Organization

######################################################################################################################


@login_required
@access_user_list
def profile_list(request):
    """
    Отображение списка пользователей
    :param request:
    :return:
    """
    current_user = get_current_user(user=request.user)
    context = {
        'current_user': current_user,
        'title': 'Список пользователей',
    }
    if request.POST:
        string_search = request.POST.get('find', '')
        organization_search = request.POST.get('organization', 0)
        organization_search = int(organization_search) if organization_search.isdigit() else 0
        total_profile, list_profile = get_list_profile(username=string_search, organization=organization_search)
        context['form_search_user'] = FormSearchUser(initial={'find': string_search})
        context['form_organization_user'] = FormOrganization(initial={'organization': organization_search})
    else:
        total_profile, list_profile = get_list_profile(username='', organization=0)
        context['form_search_user'] = FormSearchUser()
        context['form_organization_user'] = FormOrganization()
    context['total_profile'] = total_profile
    context['list_profile'] = list_profile
    return render(request, 'profile/list.html', context)


######################################################################################################################


@login_required
@access_user_list
def profile_list_organization(request, organization_id):
    """
    Отображение списка пользователей для конкретной организации
    :param request:
    :param organization_id:
    :return:
    """
    current_user = get_current_user(user=request.user)
    organization = get_object_or_404(Organization, id=organization_id)
    total_profile, list_profile = get_list_profile(username='', organization=organization_id)
    context = {
        'current_user': current_user,
        'title': 'Список пользователей',
        'form_search_user': FormSearchUser(),
        'form_organization_user': FormOrganization(initial={'organization': organization.id}),
        'total_profile': total_profile,
        'list_profile': list_profile,
    }
    return render(request, 'profile/list.html', context)


######################################################################################################################


@access_user_edit
def profile_create(request):
    """
    Создание профиля пользователя
    :param request:
    :return:
    """
    context = {
        'current_user': get_current_user(user=request.user),
        'title': 'Добавление нового пользователя',
    }
    if request.POST:
        formset = FormCreateUser(request.POST)
        username = formset['username'].value()
        password1 = formset['password'].value()
        password2 = formset['password2'].value()
        initial = {
            'email': formset['email'].value(),
            'username': username,
            'last_name': formset['last_name'].value(),
            'first_name': formset['first_name'].value(),
        }
        message_list = check_password(username, password1, password2)
        if formset.is_valid() and not message_list:
            formset.save()
            profile = UserProfile(user=get_object_or_404(User, username=username))
            profile.save()
            return redirect(reverse('profile_edit', args=(profile.id, )))
        else:
            if User.objects.filter(username=username).exists():
                del initial['username']
                message_list.append('Пользователь ' + username + ' уже существует.')
        for message in message_list:
            messages.info(request, message)
        context['form_create_user'] = FormCreateUser(initial=initial)
    else:
        context['form_create_user'] = FormCreateUser()
    return render(request, 'profile/create.html', context)


######################################################################################################################


@login_required
@access_user_list
def profile_show(request, profile_id):
    """
    Отображение профиля пользователя
    :param request:
    :param profile_id:
    :return:
    """
    profile = get_object_or_404(UserProfile, id=profile_id)
    current_user = get_current_user(user=request.user)
    context = {
        'current_user': current_user,
        'profile': profile,
        'title': 'Пользователь ' + profile.__str__(),
        'form_password': FormChangePassword(),
    }
    if request.POST and current_user.access.user_edit:
        if 'blockuser' in request.POST:
            profile.block()
        elif 'unblockuser' in request.POST:
            profile.unblock()
        elif 'changepassword' in request.POST:
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            message_list = check_password(profile.user.username, password1, password2)
            if message_list:
                for message in message_list:
                    messages.info(request, message)
                context['show_password'] = True
            else:
                profile.user.set_password(password1)
                profile.user.save()
    return render(request, 'profile/show.html', context)


######################################################################################################################


@login_required
@access_user_edit
def profile_edit(request, profile_id):
    """
    Редактирование профиля пользователя
    :param request:
    :param profile_id:
    :return:
    """
    profile = get_object_or_404(UserProfile, id=profile_id)
    if profile.user.is_superuser:
        return redirect(reverse('profile_show', args=(profile_id, )))

    if request.POST:
        formset_user = FormEditUser(request.POST, instance=profile.user)
        formset_user.save()
        formset_organization = FormOrganization(request.POST, instance=profile)
        formset_organization.save()
        access_choice = request.POST.get('access_choice', 'sample')
        if access_choice == 'sample':
            # Если выбрана определенная роль, то присваивается эта роль
            access_role = request.POST['access_role']
            access = get_object_or_404(AccessRole, id=access_role)
        else:
            # Если выбраны отдельные права, то создается новая роль с этими правами
            access = AccessRole(title=profile.user.username)
            formset_access = FormAccessList(request.POST, instance=access)
            formset_access.save()
        if profile.access and not profile.access.is_sample:
            # Если роль была не шаблонная, то она сначала удаляется, чтобы не накапливать бесхозные роли
            profile.access.delete()
        profile.access = access
        profile.save()
        return redirect(reverse('profile_show', args=(profile_id, )))
    else:
        context = {
            'current_user': get_current_user(user=request.user),
            'profile': profile,
            'title': 'Редактирование профиля ' + profile.__str__(),
            'form_edit_user': FormEditUser(instance=profile.user),
        }
        if profile.access:
            if profile.access.is_sample:
                context['form_access_role'] = FormAccessRole(initial={'access_role': profile.access.id})
            else:
                context['form_access_role'] = FormAccessRole()
            context['form_access_list'] = FormAccessList(instance=profile.access)
        else:
            context['form_access_role'] = FormAccessRole()
            context['form_access_list'] = FormAccessList()
        if profile.organization:
            context['form_organization'] = FormOrganization(initial={'organization': profile.organization})
        else:
            context['form_organization'] = FormOrganization()
        return render(request, 'profile/edit.html', context)


######################################################################################################################
