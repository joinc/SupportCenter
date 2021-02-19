# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from Organization.models import Organization, AddressOrg, SubnetOrg
from Organization.forms import FormOrganization
from Main.tools import get_current_user
from Main.decorators import access_organization_edit


######################################################################################################################


@login_required
def organization_list(request):
    """
    Вывод списка организаций
    TODO: Сделать форму поиска организаций
    :param request:
    :return:
    """
    context = {
        'current_user': get_current_user(user=request.user),
        'title': 'Список организаций',
        'organization_list': list(Organization.objects.values('id', 'short_title').all()),
    }
    return render(request=request, template_name='organization/list.html', context=context)


######################################################################################################################


@access_organization_edit
def organization_create(request):
    """
    Создание новой организации
    :param request:
    :return:
    """
    if request.POST:
        formset = FormOrganization(request.POST)
        if formset.is_valid():
            formset.save()
        return redirect(reverse('organization_list'))
    else:
        context = {
            'current_user': get_current_user(user=request.user),
            'title': 'Добавление организации',
            'form_organization': FormOrganization(),
        }
        return render(request=request, template_name='organization/create.html', context=context)


######################################################################################################################


@login_required
def organization_show(request, organization_id):
    """
    Отображение карточки организации
    :param request:
    :param organization_id:
    :return:
    """
    organization = get_object_or_404(Organization, id=organization_id)
    context = {
        'current_user': get_current_user(user=request.user),
        'title': organization.short_title,
        'organization': organization,
        'list_address': AddressOrg.objects.filter(organization=organization),
        'list_subnet': SubnetOrg.objects.filter(organization=organization),
    }
    return render(request=request, template_name='organization/show.html', context=context)


######################################################################################################################


@access_organization_edit
def organization_delete(request, organization_id):
    """
    Удаление организации
    :param request:
    :param organization_id:
    :return:
    """
    organization = get_object_or_404(Organization, id=organization_id)
    organization.delete()
    return redirect(reverse('organization_list'))


######################################################################################################################


@access_organization_edit
def organization_edit(request, organization_id):
    """
    Редактирование карточки организации
    :param request:
    :param organization_id:
    :return:
    """
    organization = get_object_or_404(Organization, id=organization_id)
    if request.POST:
        formset = FormOrganization(request.POST, instance=organization)
        if formset.is_valid():
            formset.save()
        return redirect(reverse('organization_show', args=(organization_id, )))
    else:
        context = {
            'current_user': get_current_user(user=request.user),
            'title': 'Редактирование организации',
            'organization': organization,
            'form_organization': FormOrganization(instance=organization),
        }
        return render(request=request, template_name='organization/edit.html', context=context)


######################################################################################################################
