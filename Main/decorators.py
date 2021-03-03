# -*- coding: utf-8 -*-

from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import auth
from Profile.models import Access, UserProfile

######################################################################################################################


def permission_required(list_permission):
    def check_permission(function):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if UserProfile.objects.filter(user=request.user, blocked=True).exists():
                    auth.logout(request)
                    messages.info(request, 'Выша учетная запись заблокирована, обратитесь к администратору.')
                    return redirect(reverse('login'))
                for permission in list_permission:
                    if Access.objects.filter(
                            permission__name=permission,
                            preset__PresetAccess_UserProfile__user=request.user,
                    ).exists():
                        return function(request, *args, **kwargs)
                return redirect(reverse('index'))
            return redirect(reverse('login'))
        return wrapper
    return check_permission


######################################################################################################################
