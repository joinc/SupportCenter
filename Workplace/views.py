# -*- coding: utf-8 -*-

from django.shortcuts import render
from Main.tools import get_profile

######################################################################################################################


def workplace_list(request):
    """

    :param request:
    :return:
    """
    context = {
        'current_user': get_profile(user=request.user),
    }
    return render(request=request, template_name='signature/list.html', context=context)


######################################################################################################################
