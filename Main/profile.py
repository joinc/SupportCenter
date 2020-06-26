# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Organization
from .forms import FormUser


######################################################################################################################


@login_required
def profile_list(request):
    context = {'profile': get_object_or_404(UserProfile, user=request.user),
               'profile_list': list(UserProfile.objects.all())}
    return render(request, 'profile_list.html', context)

######################################################################################################################


@login_required
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
        context['form_user'] = FormUser(
            initial={
                'username': request.user,
                'last_name': request.user.last_name,
                'first_name': request.user.first_name,
            }
        )
        return render(request, 'profile_create.html', context)


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
