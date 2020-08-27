# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from Organization.models import Organization
from Organization.forms import FormOrganization
from Main.tools import get_current_user
from Main.decorators import access_organization_edit


######################################################################################################################


@login_required
def organization_list(request):
    if request.POST:
        return organization_create(request)
    else:
        context = {
            'current_user': get_current_user(request),
            'organization_list': list(Organization.objects.values('id', 'short_title').all()),
            'form_organization': FormOrganization(),
        }
        return render(request, 'organization/list.html', context)


######################################################################################################################


@access_organization_edit
def organization_create(request):
    if request.POST:
        formset = FormOrganization(request.POST)
        if formset.is_valid():
            formset.save()
        return redirect(reverse('organization_list'))
    else:
        context = {
            'current_user': get_current_user(request),
            'form_organization': FormOrganization(),
        }
        return render(request, 'organization/create.html', context)


######################################################################################################################


@login_required
def organization_show(request, organization_id):
    context = {
        'current_user': get_current_user(request),
        'organization': get_object_or_404(Organization, id=organization_id),
    }
    return render(request, 'organization/show.html', context)


######################################################################################################################


@access_organization_edit
def organization_delete(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)
    organization.delete()
    return redirect(reverse('organization_list'))


######################################################################################################################


@access_organization_edit
def organization_edit(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)
    if request.POST:
        formset = FormOrganization(request.POST, instance=organization)
        if formset.is_valid():
            formset.save()
        return redirect(reverse('organization_show', args=(organization_id, )))
    else:
        context = {
            'current_user': get_current_user(request),
            'organization': organization,
            'form_organization': FormOrganization(instance=organization),
        }
        return render(request, 'organization/edit.html', context)


######################################################################################################################
