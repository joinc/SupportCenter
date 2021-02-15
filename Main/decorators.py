# -*- coding: utf-8 -*-

from django.shortcuts import redirect, reverse
from Main.tools import get_current_user


######################################################################################################################


def access_user_list(function):
    def _inner(request, *args, **kwargs):
        profile = get_current_user(request)
        if not profile.access.user_list:
            return redirect(reverse('index'))
        else:
            return function(request, *args, **kwargs)
    return _inner


######################################################################################################################


def access_user_edit(function):
    def _inner(request, *args, **kwargs):
        profile = get_current_user(request)
        if not profile.access.user_edit:
            return redirect(reverse('index'))
        else:
            return function(request, *args, **kwargs)
    return _inner


######################################################################################################################


def access_esign_list(function):
    def _inner(request, *args, **kwargs):
        profile = get_current_user(request)
        if not profile.access.signature_list:
            return redirect(reverse('index'))
        else:
            return function(request, *args, **kwargs)
    return _inner


######################################################################################################################


def access_esign_edit(function):
    def _inner(request, *args, **kwargs):
        profile = get_current_user(request)
        if not profile.access.esign_edit:
            return redirect(reverse('index'))
        else:
            return function(request, *args, **kwargs)
    return _inner


######################################################################################################################


def access_organization_edit(function):
    def _inner(request, *args, **kwargs):
        profile = get_current_user(request)
        if not profile.access.organization_edit:
            return redirect(reverse('index'))
        else:
            return function(request, *args, **kwargs)
    return _inner


######################################################################################################################
