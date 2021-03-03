# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from Organization.models import Organization, OrganizationAddress, OrganizationSubnet
from Organization.forms import FormOrganization, FormAddress, FormSubnet
from Main.decorators import permission_required
from Main.tools import get_profile

######################################################################################################################


@permission_required(['organization_list', ])
def organization_list(request):
    """
    Вывод списка организаций
    TODO: Сделать форму поиска организаций
    :param request:
    :return:
    """
    current_user = get_profile(user=request.user)
    context = {
        'current_user': current_user,
        'title': 'Список организаций',
        'organization_list': list(Organization.objects.values('id', 'short_title').all()),
        'organization_edit': current_user.access(list_permission=['organization_edit', ])
    }
    return render(request=request, template_name='organization/list.html', context=context)


######################################################################################################################


@permission_required(['organization_edit', ])
def organization_create(request):
    """
    Создание новой организации
    :param request:
    :return:
    """
    if request.POST:
        organization = Organization()
        formset = FormOrganization(request.POST, instance=organization)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Организация {0} успешно создана.'.format(organization.short_title))
            return redirect(reverse('organization_edit', args=(organization.id, )))
        else:
            messages.error(request, 'Ошибка при создании организации.')
            return redirect(reverse('organization_list'))
    else:
        context = {
            'current_user': get_profile(user=request.user),
            'title': 'Добавление организации',
            'form_organization': FormOrganization(),
        }
        return render(request=request, template_name='organization/create.html', context=context)


######################################################################################################################


@permission_required(['organization_edit', ])
def organization_address_create(request, organization_id):
    """
    Добавление адреса к организации
    :param request:
    :param organization_id:
    :return:
    """
    if request.POST:
        organization = get_object_or_404(Organization, id=organization_id)
        organization_address = OrganizationAddress(organization=organization)
        formset = FormAddress(request.POST, instance=organization_address)
        if formset.is_valid():
            if OrganizationAddress.objects.filter(
                    organization=organization_address.organization,
                    address=organization_address.address,
            ).exists():
                messages.error(request, 'Адрес {0} уже указан для организации {1}'.format(
                    organization_address.address,
                    organization_address.organization,
                ))
            else:
                formset.save()
                messages.success(request, 'Адрес {0} добавлен к организации {1}'.format(
                    organization_address.address,
                    organization_address.organization,
                ))
        else:
            messages.error(request, 'Ошибка добавления адреса. Не корректно заполнена форма.')
    return redirect(reverse('organization_edit', args=(organization_id, )))


######################################################################################################################


@permission_required(['organization_edit', ])
def organization_subnet_create(request, organization_id):
    """
    Добавление подсети к организации
    :param request:
    :param organization_id:
    :return:
    """
    if request.POST:
        organization = get_object_or_404(Organization, id=organization_id)
        organization_subnet = OrganizationSubnet(organization=organization)
        formset = FormSubnet(request.POST, instance=organization_subnet)
        if formset.is_valid():
            if OrganizationSubnet.objects.filter(
                    organization=organization_subnet.organization,
                    subnet=organization_subnet.subnet,
            ).exists():
                messages.error(request, 'Подсеть {0} уже указана для организации {1}'.format(
                    organization_subnet.subnet,
                    organization_subnet.organization,
                ))
            else:
                formset.save()
                messages.success(request, 'Подсеть {0} добавлена к организации {1}'.format(
                    organization_subnet.subnet,
                    organization_subnet.organization,
                ))
        else:
            messages.error(request, 'Ошибка добавления подсети. Не корректно заполнена форма.')
    return redirect(reverse('organization_edit', args=(organization_id, )))


######################################################################################################################


@permission_required(['organization_list', ])
def organization_show(request, organization_id):
    """
    Отображение карточки организации
    :param request:
    :param organization_id:
    :return:
    """
    organization = get_object_or_404(Organization, id=organization_id)
    current_user = get_profile(user=request.user)
    context = {
        'current_user': current_user,
        'title': organization.short_title,
        'organization': organization,
        'list_address': OrganizationAddress.objects.filter(organization=organization),
        'list_subnet': OrganizationSubnet.objects.filter(organization=organization),
        'organization_edit': current_user.access(list_permission=['organization_edit', ])
    }
    return render(request=request, template_name='organization/show.html', context=context)


######################################################################################################################


@permission_required(['organization_edit', ])
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
            messages.success(request, '')
        else:
            messages.error(request, '')
        return redirect(reverse('organization_show', args=(organization_id, )))
    else:
        context = {
            'current_user': get_profile(user=request.user),
            'title': 'Редактирование организации',
            'organization': organization,
            'form_organization': FormOrganization(instance=organization),
            'form_address': FormAddress(),
            'form_subnet': FormSubnet(),
            'list_address': OrganizationAddress.objects.filter(organization=organization),
            'list_subnet': OrganizationSubnet.objects.filter(organization=organization),
        }
        return render(request=request, template_name='organization/edit.html', context=context)


######################################################################################################################


@permission_required(['organization_edit', ])
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


@permission_required(['organization_edit', ])
def organization_address_delete(request, org_address_id):
    """
    Удаление адреса организации
    :param request:
    :param org_address_id:
    :return:
    """
    organization_address = get_object_or_404(OrganizationAddress, id=org_address_id)
    organization = organization_address.organization
    organization_address.delete()
    return redirect(reverse('organization_edit', args=(organization.id, )))


######################################################################################################################


@permission_required(['organization_edit', ])
def organization_subnet_delete(request, org_subnet_id):
    """
    Удаление подсети организации
    :param request:
    :param org_subnet_id:
    :return:
    """
    organization_subnet = get_object_or_404(OrganizationSubnet, id=org_subnet_id)
    organization = organization_subnet.organization
    organization_subnet.delete()
    return redirect(reverse('organization_edit', args=(organization.id, )))


######################################################################################################################
