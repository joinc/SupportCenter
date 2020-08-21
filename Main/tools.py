# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from Profile.models import UserProfile


######################################################################################################################


def get_current_user(request):
    return get_object_or_404(UserProfile, user=request.user)


######################################################################################################################
