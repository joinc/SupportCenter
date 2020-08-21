# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Main.models import Organization
from Profile.models import UserProfile, AccessRole
from Profile.forms import FormUser, FormPassword, FormAccess, FormUserSearch
from Main.decorators import access_user_edit, access_user_list
from Main.tools import get_current_user


######################################################################################################################


def profile_create(request, context):
    username = request.POST['username']
    email = request.POST['email']
    last_name = request.POST['last_name']
    first_name = request.POST['first_name']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    access_role = request.POST['access_role']
    organization = request.POST['organization']
    initial = {
        'email': email,
        'username': username,
        'last_name': last_name,
        'first_name': first_name,
        'access_role': access_role,
        'organization': organization,
    }
    if User.objects.filter(username=username).exists():
        del initial['username']
        messages.info(request, 'Пользователь ' + username + ' уже существует.')
    elif password1 != password2:
        messages.info(request, 'Пароли не совпадают.')
    elif len(password2) < 8:
        messages.info(request, 'Длина пароля менее 8 символов.')
    elif password2.isdigit():
        messages.info(request, 'Пароль состоит только из цифр.')
    elif password2 == username:
        messages.info(request, 'Пароль совпадает с логином.')
    else:
        new_user = User.objects.create_user(
            username=username,
            email=email,
            password=password2,
            first_name=first_name,
            last_name=last_name,
        )
        new_user.save()
        new_profile = UserProfile()
        new_profile.user = new_user
        new_profile.organization = get_object_or_404(Organization, id=organization)
        new_profile.access = get_object_or_404(AccessRole, id=access_role)
        new_profile.save()
        return context
    context['form_user'] = FormUser(initial=initial)
    context['show_form_user'] = True
    return context


######################################################################################################################


@login_required
@access_user_list
def profile_list(request):
    current_user = get_current_user(request)
    context = {
        'current_user': current_user,
        'profiles_total': UserProfile.objects.count(),
        'form_user': FormUser(),
        'form_password': FormPassword(),
        'form_user_search': FormUserSearch(),

    }
    if request.POST and current_user.access.user_edit:
        if "adduser" in request.POST:
            context = profile_create(request, context)
            profiles_list = UserProfile.objects.all()[:20]
        if "search" in request.POST:
            search_string = request.POST.get('find', '')
            if search_string != '':
                profiles_list = (list(UserProfile.objects.filter(user__username__contains=search_string))
                                 + list(UserProfile.objects.filter(user__last_name__contains=search_string)))[:20]
                context['form_user_search'] = FormUserSearch(
                    initial={
                        'find': search_string,
                    }
                )
            else:
                return redirect(reverse('profile_list', ))
    else:
        profiles_list = UserProfile.objects.all()[:20]
    context['profiles_count'] = len(profiles_list)
    context['profiles_list'] = profiles_list

    return render(request, 'profile/list.html', context)


######################################################################################################################


@login_required
@access_user_list
def profile_show(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    current_user = get_current_user(request)
    context = {
        'current_user': current_user,
        'profile': profile,
        'form_password': FormPassword(),
    }
    if request.POST and current_user.access.user_edit:
        if 'blockuser' in request.POST:
            profile.blocked = True
            profile.save()
        elif 'unblockuser' in request.POST:
            profile.blocked = False
            profile.save()
        elif 'changepassword' in request.POST:
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            message = None
            if password1 != password2:
                message = 'Пароли не совпадают.'
            elif len(password2) < 8:
                message = 'Длина пароля менее 8 символов.'
            elif password2.isdigit():
                message = 'Пароль состоит только из цифр.'
            elif password2 == profile.user.username:
                message = 'Пароль совпадает с логином.'
            if message:
                messages.info(request, message)
                context['show_password'] = True
            else:
                profile.user.set_password(password2)
                profile.user.save()
    return render(request, 'profile/show.html', context)


######################################################################################################################


@login_required
@access_user_edit
def profile_edit(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    if profile.user.is_superuser:
        return redirect(reverse('index'))
    context = {
        'current_user': get_current_user(request),
        'profile': profile,
        'form_user': FormUser(
            initial={
                'email': profile.user.email,
                'username': profile.user.username,
                'last_name': profile.user.last_name,
                'first_name': profile.user.first_name,
                'access_role': profile.access.id,
                'organization': profile.organization.id,
            }
        ),
        'form_access': FormAccess(
            initial={
                'access_user_list': profile.access.user_list,
                'access_user_edit': profile.access.user_edit,
                'access_esign_list': profile.access.esign_list,
                'access_esign_edit': profile.access.esign_edit,
                'access_esign_moderator': profile.access.esign_moderator,
            }
        ),
        'sample': profile.access.is_sample,
    }
    if request.POST:
        email = request.POST['email']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        organization = request.POST['organization']
        access_choice = request.POST.get('access_choice', 'sample')
        access_role = request.POST['access_role']
        profile.user.email = email
        profile.user.first_name = first_name
        profile.user.last_name = last_name
        profile.organization = get_object_or_404(Organization, id=organization)
        if access_choice == 'sample':
            # Если выбрана определенная роль, то присваивается эта роль
            access = get_object_or_404(AccessRole, id=access_role)
        else:
            # Если выбраны отдельные права, то создается новая роль с этими правами
            access = AccessRole(
                user_list=bool(request.POST.get('access_user_list', False)),
                user_edit=bool(request.POST.get('access_user_edit', False)),
                esign_list=bool(request.POST.get('access_esign_list', False)),
                esign_edit=bool(request.POST.get('access_esign_edit', False)),
                esign_moderator=bool(request.POST.get('access_esign_moderator', False)),
                title=profile.user.username,
            )
            access.save()
        if profile.access.is_sample:
            # Если роль была шаблонная, то она просто меняется на новую
            profile.access = access
        else:
            # Если роль была не шаблонная, то она сначала удаляется, чтобы не накапливать бесхозные роли
            profile.access.delete()
            profile.access = access
        profile.user.save()
        profile.save()
        return redirect(reverse('profile_show', args=(profile_id, )))
    return render(request, 'profile/edit.html', context)


######################################################################################################################
