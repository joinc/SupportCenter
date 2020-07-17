# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect, reverse
from Profile.models import UserProfile


######################################################################################################################


def access_user_list(function):
    def _inner(request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        if not profile.access.user_list:
            return redirect(reverse('index'))
        else:
            return function(request, *args, **kwargs)
    return _inner


######################################################################################################################


def access_user_edit(function):
    def _inner(request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        if not profile.access.user_edit:
            return redirect(reverse('index'))
        else:
            return function(request, *args, **kwargs)
    return _inner


######################################################################################################################


def access_esign_list(function):
    def _inner(request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        if not profile.access.esign_list:
            return redirect(reverse('index'))
        else:
            return function(request, *args, **kwargs)
    return _inner


######################################################################################################################


def access_esign_edit(function):
    def _inner(request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        if not profile.access.esign_edit:
            return redirect(reverse('index'))
        else:
            return function(request, *args, **kwargs)
    return _inner


######################################################################################################################
