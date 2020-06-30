# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth, User
from .models import UserProfile, Organization, AccessRole
from .forms import FormUser
from .decorators import access_user_edit, access_user_list


######################################################################################################################


@login_required
@access_user_list
def profile_list(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        'profile': profile,
        'profile_list': list(UserProfile.objects.all()),
        'form_user': FormUser(),
    }
    if request.POST:
        if "adduser" in request.POST:
            username = request.POST['username']
            last_name = request.POST['last_name']
            first_name = request.POST['first_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            access_role = request.POST['access_role']
            organization = request.POST['organization']
            initial = {
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
                new_user = User.objects.create_user(username=username, email='', password=password2)
                new_user.last_name = last_name
                new_user.first_name = first_name
                new_user.save()
                new_profile = UserProfile()
                new_profile.user = new_user
                new_profile.organization = get_object_or_404(Organization, id=organization)
                new_profile.access = get_object_or_404(AccessRole, id=access_role)
                new_profile.save()
                # context['toast'] = 'Создана учетная запись пользователя ' + new_user.get_full_name() + '.'
                # return render(request, 'profile_list.html', context)
                return redirect(reverse('profile_list'))
            context['form_user'] = FormUser(initial=initial)
            context['show_user'] = True
            return render(request, 'profile_list.html', context)
        elif 'blockuser' in request.POST:
            if profile.access.user_edit:
                user = get_object_or_404(UserProfile, user=request.POST['useridblock'])
                user.blocked = True
                user.save()
                return redirect(reverse('profile_list'))
        elif 'unblockuser' in request.POST:
            if profile.access.user_edit:
                user = get_object_or_404(UserProfile, user=request.POST['useridunblock'])
                user.blocked = False
                user.save()
                return redirect(reverse('profile_list'))
    return render(request, 'profile_list.html', context)

######################################################################################################################


@login_required
@access_user_edit
def profile_create(request):
    context = {'profile': get_object_or_404(UserProfile, user=request.user), }
    if request.POST:
        profile = UserProfile.objects.filter(user=request.user).first()
        organization = Organization.objects.filter(id=request.POST['organization']).first()
        if profile:
            if organization:
                profile.organization = organization
                profile.save()
        else:
            if organization:
                new_profile = UserProfile()
                new_profile.user = request.user
                new_profile.organization = organization
                new_profile.save()
        return redirect(reverse('index'))
    else:
        return redirect(reverse('profile_list'))


######################################################################################################################


@login_required
def profile_show(request, profile_id):
    context = {'profile': get_object_or_404(UserProfile, id=profile_id)}
    return render(request, 'profile_show.html', context)


######################################################################################################################


@login_required
def profile_edit(request, profile_id):
    context = {'profile': get_object_or_404(UserProfile, id=profile_id)}
    return render(request, 'profile_list.html', context)


######################################################################################################################


@login_required
def profile_delete(request, profile_id):
    context = {'profile': get_object_or_404(UserProfile, id=profile_id)}
    return render(request, 'profile_list.html', context)

######################################################################################################################
