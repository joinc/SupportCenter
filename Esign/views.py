# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from Profile.models import UserProfile

######################################################################################################################


@login_required
def esign_list(request):
    # Главная страница
    context = {'current_user': get_object_or_404(UserProfile, user=request.user), }
    return render(request, 'esign/list.html', context)


######################################################################################################################
