from django.shortcuts import render
from Main.tools import get_current_user


def workplace_list(request):
    context = {
        'current_user': get_current_user(request),
    }
    return render(request, 'esign/list.html', context)
