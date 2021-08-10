# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from Profile.models import UserProfile, PresetAccess, Permission, Access
from Profile.tools import get_list_profile, check_password
from Profile.forms import FormChangePassword, FormSearchUser, FormOrganization, FormCreateUser, FormEditUser, \
    FormPresetAccess
from Main.decorators import permission_required
from Main.tools import get_profile, get_list_access
from Organization.models import Organization

######################################################################################################################


@permission_required(['profile_list', 'profile_edit', ])
def profile_list(request):
    """
    Отображение списка пользователей
    :param request:
    :return:
    """
    current_user = get_profile(user=request.user)
    context = {
        'current_user': current_user,
        'title': 'Список пользователей',
        'profile_edit': current_user.access(list_permission=['profile_edit', ]),
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
    return render(request=request, template_name='profile/list.html', context=context)


######################################################################################################################


@permission_required(['profile_list', 'profile_edit', ])
def profile_list_organization(request, organization_id):
    """
    Отображение списка пользователей для конкретной организации
    :param request:
    :param organization_id:
    :return:
    """
    current_user = get_profile(user=request.user)
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
    return render(request=request, template_name='profile/list.html', context=context)


######################################################################################################################


@permission_required(['profile_edit', ])
def profile_create(request):
    """
    Создание профиля пользователя
    :param request:
    :return:
    """
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
            messages.error(request, message)
        form_create_user = FormCreateUser(initial=initial)
    else:
        form_create_user = FormCreateUser()
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Добавление нового пользователя',
        'list_breadcrumb': (
            (reverse('profile_list'), 'Список пользователей'),
        ),
        'form_create_user': form_create_user,
    }
    return render(request=request, template_name='profile/create.html', context=context)


######################################################################################################################


@permission_required(['profile_list', 'profile_edit', ])
def profile_show(request, profile_id):
    """
    Отображение профиля пользователя
    :param request:
    :param profile_id:
    :return:
    """
    profile = get_object_or_404(UserProfile, id=profile_id)
    current_user = get_profile(user=request.user)
    context = {
        'current_user': current_user,
        'profile': profile,
        'title': 'Пользователь ' + profile.__str__(),
        'list_breadcrumb': (
            (reverse('profile_list'), 'Список пользователей'),
        ),
        'form_password': FormChangePassword(),
        'profile_edit': current_user.access(list_permission=['profile_edit', ]),
    }
    if request.POST and (current_user.access(list_permission=['profile_edit', ]) or current_user == profile):
        if 'block_user' in request.POST:
            profile.block()
            messages.warning(request, 'Пользователь {0} заблокирован.'.format(profile))
        elif 'unblock_user' in request.POST:
            profile.unblock()
            messages.warning(request, 'Пользователь {0} разблокирован.'.format(profile))
        elif 'change_password' in request.POST:
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            message_list = check_password(profile.user.username, password1, password2)
            if message_list:
                for message in message_list:
                    messages.error(request, message)
                context['show_password'] = True
            else:
                messages.success(request, 'Пароль пользователя {0} успешно сменен.'.format(profile))
                profile.user.set_password(password1)
                profile.user.save()
    return render(request=request, template_name='profile/show.html', context=context)


######################################################################################################################


@permission_required(['profile_edit', ])
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
        FormEditUser(request.POST, instance=profile.user).save()
        FormOrganization(request.POST, instance=profile).save()
        access_choice = request.POST.get('access_choice', 'not_sample')
        if access_choice == 'sample':
            # Если выбран определенный набор прав, то присваивается этот роль
            preset_access = request.POST.get('preset_access', None)
            if preset_access:
                preset = get_object_or_404(PresetAccess, id=preset_access)
            else:
                messages.error(request, 'Не правильно указана роль доступа пользователя {0}.'.format(profile))
                return redirect(reverse('profile_edit', args=(profile_id,)))
        else:
            # Если выбраны отдельные права, то создается новая роль с этими правами
            preset = PresetAccess(title=profile.user.username, is_sample=False, )
            preset.save()
            for permission in Permission.objects.all():
                access = request.POST.get(permission.name, False)
                if access:
                    Access(permission=permission, preset=preset, value=True).save()
        old_preset = profile.preset
        profile.preset = preset
        profile.save(update_fields=['preset', ])
        if old_preset and not old_preset.is_sample:
            # Если роль была не шаблонная, то она удаляется, чтобы не накапливать бесхозные роли
            old_preset.delete()
        messages.success(request, 'Профиль пользователя {0} успешно сохранен.'.format(profile))
        return redirect(reverse('profile_show', args=(profile_id, )))
    else:
        context = {
            'current_user': get_profile(user=request.user),
            'profile': profile,
            'title': 'Редактирование профиля ' + profile.__str__(),
            'list_breadcrumb': (
                (reverse('profile_list'), 'Список пользователей'),
                (reverse('profile_show', args=(profile.id, )), 'Пользователь {0}'.format(profile)),
            ),
            'form_edit_user': FormEditUser(instance=profile.user),
            'list_access': get_list_access(preset=profile.preset),
            'form_preset_access': FormPresetAccess(initial={'preset_access': profile.preset_id}),
            'form_organization': FormOrganization(initial={'organization': profile.organization}),
        }
        return render(request=request, template_name='profile/edit.html', context=context)


######################################################################################################################
