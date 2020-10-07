# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Profile.models import UserProfile, AccessRole
from Profile.forms import FormChangePassword, FormSearchUser, FormAccessList, FormOrganization, FormCreateUser, FormEditUser, FormAccessRole
from Main.decorators import access_user_edit, access_user_list
from Main.tools import get_current_user


######################################################################################################################


def check_password(username, password1, password2):
    message_list = []
    if password1 != password2:
        message_list.append('Пароли не совпадают.')
    if len(password1) < 8:
        message_list.append('Длина пароля менее 8 символов.')
    if password1.isdigit():
        message_list.append('Пароль состоит только из цифр.')
    if password1 == username:
        message_list.append('Пароль совпадает с логином.')
    return message_list


######################################################################################################################


@login_required
@access_user_list
def profile_list(request):
    current_user = get_current_user(request)
    context = {
        'current_user': current_user,
        'title': 'Список пользователей',
        'profiles_total': UserProfile.objects.count(),
        'form_search_user': FormSearchUser(),
    }
    if request.POST:
        if "adduser" in request.POST:
            context = profile_create(request, context)
            profiles_list = UserProfile.objects.all()[:20]
        if "search" in request.POST:
            return profile_search(request, context)
    else:
        profiles_list = UserProfile.objects.all()[:20]
    context['profiles_count'] = len(profiles_list)
    context['profiles_list'] = profiles_list
    return render(request, 'profile/list.html', context)


######################################################################################################################


@access_user_edit
def profile_create(request):
    context = {
        'current_user': get_current_user(request),
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


@access_user_list
def profile_search(request, context):
    search_string = request.POST.get('find', '')
    if search_string != '':
        profiles_list = (list(UserProfile.objects.filter(user__username__contains=search_string))
                         + list(UserProfile.objects.filter(user__last_name__contains=search_string)))[:20]
        context['form_search_user'] = FormSearchUser(
            initial={
                'find': search_string,
            }
        )
        context['profiles_count'] = len(profiles_list)
        context['profiles_list'] = profiles_list
        return render(request, 'profile/list.html', context)
    else:
        return redirect(reverse('profile_list'))


######################################################################################################################


@login_required
@access_user_list
def profile_show(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    current_user = get_current_user(request)
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
    profile = get_object_or_404(UserProfile, id=profile_id)
    if profile.user.is_superuser:
        return redirect(reverse('profile_list'))

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
            'current_user': get_current_user(request),
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
