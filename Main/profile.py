# -*- coding: utf-8 -*-

from .models import UserProfile
from django.shortcuts import render
from .forms import FormUser


######################################################################################################################


def profile_create(request):
    form_user = FormUser(initial={'username': request.user, })
    context = {'form_user': form_user, }
    return render(request, 'profile_create.html', context)


######################################################################################################################
