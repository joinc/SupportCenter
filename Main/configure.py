# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from Main.tools import get_current_user
from Profile.models import PresetAccess

######################################################################################################################


@login_required
def configure_list(request):
    """
    Отображение списка настроек
    :param request:
    :return: HttpResponse
    """
    if request.user.is_superuser:

        current_user = get_current_user(request=request)
        context = {
            'current_user': current_user,
            'title': 'Список конфигураций',
        }
        return render(request=request, template_name='configure/list.html', context=context)
    return redirect(reverse('index'))


######################################################################################################################

def preset_list(request):
    context = {
        'current_user': get_current_user(request=request),
        'title': 'Шаблоны',
        'list_preset': PresetAccess.objects.filter(is_sample=True, )
    }
    return render(request, template_name='configure/preset_list.html', context=context)
