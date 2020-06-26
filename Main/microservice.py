# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Organization


######################################################################################################################


@login_required
def organization_list(request, org_title):
    organizations = Organization.objects.values('id', 'short_title').filter(short_title__icontains=org_title)
    return JsonResponse({'organization_list': list(organizations)})


######################################################################################################################


@login_required
def organization_all(request):
    organizations = Organization.objects.values('id', 'short_title').all()
    return JsonResponse({'organization_list': list(organizations)})

######################################################################################################################
