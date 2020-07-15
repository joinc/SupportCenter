# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from Profile.models import UserProfile
from Esign.models import Certificate
from Esign.forms import FormUpload

######################################################################################################################


@login_required
def esign_list(request):
    # Список электронных подписей
    current_user = get_object_or_404(UserProfile, user=request.user)
    context = {
        'current_user': current_user,
        'form_upload': FormUpload(),
        'esign_total': Certificate.objects.filter(owner=current_user).count(),
        'esign_list': Certificate.objects.filter(owner=current_user),
    }
    return render(request, 'esign/list.html', context)


######################################################################################################################
