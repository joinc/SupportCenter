# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from Profile.models import UserProfile


######################################################################################################################


def get_current_user(user) -> UserProfile:
    """

    :param user:
    :return:
    """
    return get_object_or_404(UserProfile, user=user)


######################################################################################################################
