from django.shortcuts import render
from Main.tools import get_current_user


def workplace_list(request):
    """

    :param request:
    :return:
    """
    context = {
        'current_user': get_current_user(user=request.user),
    }
    return render(request=request, template_name='signature/list.html', context=context)
