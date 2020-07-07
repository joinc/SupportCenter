# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth, User
from .models import UserProfile, Organization, AccessRole
from .forms import FormUser, FormChangePassword, FormAccess
from .decorators import access_user_edit, access_user_list


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
        return redirect(reverse('profile_list'))
    context['form_user'] = FormUser(initial=initial)
    context['show_form_user'] = True
    return render(request, 'profile_list.html', context)


######################################################################################################################


@login_required
@access_user_list
def profile_list(request):
    current_user = get_object_or_404(UserProfile, user=request.user)
    profiles_list = UserProfile.objects.all()
    context = {
        'current_user': current_user,
        'profiles_list': profiles_list,
        'profiles_count': profiles_list.count(),
        'form_user': FormUser(),
        'form_change_password': FormChangePassword(),
    }
    if request.POST and current_user.access.user_edit:
        if "adduser" in request.POST:
            return profile_create(request, context)
    return render(request, 'profile_list.html', context)


######################################################################################################################


@login_required
def profile_show(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    current_user = get_object_or_404(UserProfile, user=request.user)
    if profile != current_user and not current_user.access.user_edit:
        return redirect(reverse('index'))
    context = {
        'current_user': current_user,
        'profile': profile,
        'form_change_password': FormChangePassword(),
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
    return render(request, 'profile_show.html', context)


######################################################################################################################


@login_required
@access_user_edit
def profile_edit(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    if profile.user.is_superuser:
        return redirect(reverse('index'))
    current_user = get_object_or_404(UserProfile, user=request.user)
    context = {
        'current_user': current_user,
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
            }
        ),
    }
    if request.POST:
        email = request.POST['email']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        organization = request.POST['organization']
        access = request.POST['access']
        access_role = request.POST['access_role']
        profile.user.email = email
        profile.user.first_name = first_name
        profile.user.last_name = last_name
        profile.user.save()
        profile.organization = get_object_or_404(Organization, id=organization)
        profile.access = get_object_or_404(AccessRole, id=access_role)
        profile.save()
        return redirect(reverse('profile_show', args=(profile_id, )))
    return render(request, 'profile_edit.html', context)


######################################################################################################################
