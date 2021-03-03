# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from Profile.models import UserProfile, Permission, Access
from Main.choices import CATEGORY_PERMISSION

######################################################################################################################


def get_profile(user) -> UserProfile:
    """

    :param user:
    :return:
    """
    return get_object_or_404(UserProfile, user=user)


######################################################################################################################


def get_list_access(preset):
    """

    :param preset:
    :return:
    """
    list_access = []
    for category_id, category_title in CATEGORY_PERMISSION:
        list_permission = []
        for permission in Permission.objects.filter(category=category_id):
            if Access.objects.filter(permission=permission, preset=preset).exists():
                list_permission.append([
                    permission.title,
                    permission.name,
                    Access.objects.get(permission=permission, preset=preset).value,
                ])
            else:
                list_permission.append([
                    permission.title,
                    permission.name,
                    False,
                ])
        list_access.append([category_title, list_permission])
    return list_access


######################################################################################################################
