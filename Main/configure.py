# -*- coding: utf-8 -*-

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, reverse
from Main.tools import get_list_access, get_profile
from Main.forms import FormPresetTitle, FormAddress, FormSubnet
from Main.decorators import permission_required
from Profile.models import PresetAccess, Permission, Access
from Workplace.models import Address, Subnet

######################################################################################################################


@permission_required(['configure_edit', ])
def configure_list(request):
    """
    Отображение списка настроек
    :param request:
    :return: HttpResponse
    """
    list_configure = {
        'Профиль пользователя': {
            'Список шаблонов разрешений': 'preset_list',
        },
        'Организации': {
            'Список адресов': 'address_list',
            'Список подсетей': 'subnet_list',
        },
    }
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Список конфигураций',
        'list_configure': list_configure,
    }
    return render(request=request, template_name='configure/configure_list.html', context=context)


######################################################################################################################


@permission_required(['configure_edit', ])
def preset_list(request):
    """
    Отображение списка шаблоново разрешений
    :param request:
    :return:
    """
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Список шаблонов разрешений',
        'list': PresetAccess.objects.filter(is_sample=True, ),
        'url_create': 'preset_create',
        'title_create': 'Добавить новый шаблон',
        'url_edit': 'preset_edit',
        'title_edit': 'Перейти к редактированию шаблона',
    }
    return render(request=request, template_name='configure/list.html', context=context)


######################################################################################################################


@permission_required(['configure_edit', ])
def address_list(request):
    """
    Отображение списка адресов
    :param request:
    :return:
    """
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Список адресов',
        'list': Address.objects.all(),
        'url_create': 'address_create',
        'title_create': 'Добавить новый адрес',
        'url_edit': 'address_edit',
        'title_edit': 'Перейти к редактированию адреса',
    }
    return render(request=request, template_name='configure/list.html', context=context)


######################################################################################################################


@permission_required(['configure_edit', ])
def subnet_list(request):
    """
    Отображение списка подсетей
    :param request:
    :return:
    """
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Список подсетей',
        'list': Subnet.objects.all(),
        'url_create': 'subnet_create',
        'title_create': 'Добавить новую подсеть',
        'url_edit': 'subnet_edit',
        'title_edit': 'Перейти к редактированию подсети',
    }
    return render(request=request, template_name='configure/list.html', context=context)


######################################################################################################################


@permission_required(['configure_edit', ])
def preset_create(request):
    """
    Создание нового шаблона разрешений
    :param request:
    :return:
    """
    if request.POST:
        preset = PresetAccess(is_sample=True)
        formset = FormPresetTitle(request.POST, instance=preset)
        if formset.is_valid():
            if PresetAccess.objects.filter(title=preset.title).exists():
                messages.error(request, 'Шаблон разрешений с этим названием уже существует.')
            else:
                formset.save()
                messages.info(request, 'Новый шаблон разрешений {0} создан.'.format(preset))
                return redirect(reverse('preset_edit', args=(preset.id,)))
        else:
            messages.error(request, 'Укажите название шаблона разрешений.')
    else:
        formset = FormPresetTitle()
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Создание шаблона разрешений',
        'form_preset_title': formset,
    }
    return render(request=request, template_name='configure/preset_create.html', context=context)


######################################################################################################################


@permission_required(['configure_edit', ])
def address_create(request):
    """
    Создание нового адреса
    :param request:
    :return:
    """
    if request.POST:
        formset = FormAddress(request.POST)
        if formset.is_valid():
            formset.save()
            messages.info(request, 'Новый адрес создан.')
            return redirect(reverse('address_list'))
        else:
            messages.error(request, 'Ошибка при создании адреса.')
    else:
        formset = FormAddress()
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Создание адреса',
        'url_breadcrumb': 'address_list',
        'title_breadcrumb': 'Список адресов',
        'formset': formset,
    }
    return render(request=request, template_name='configure/create.html', context=context)


######################################################################################################################


@permission_required(['configure_edit', ])
def subnet_create(request):
    """
    Создание новой подсети
    :param request:
    :return:
    """
    if request.POST:
        subnet = Subnet()
        formset = FormSubnet(request.POST, instance=subnet)
        if formset.is_valid():
            if Subnet.objects.filter(subnet=subnet.subnet).exists():
                messages.error(request, 'Подсеть {0} уже существует.'.format(subnet))
            else:
                formset.save()
                messages.info(request, 'Новая подсеть {0} создана.'.format(subnet))
                return redirect(reverse('subnet_list'))
        else:
            messages.error(request, 'Ошибка при создании подсети.')
    else:
        formset = FormSubnet()
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Создание подсети',
        'url_breadcrumb': 'subnet_list',
        'title_breadcrumb': 'Список подсетей',
        'formset': formset,
    }
    return render(request=request, template_name='configure/create.html', context=context)


######################################################################################################################


@permission_required(['configure_edit', ])
def preset_edit(request, preset_id):
    """
    Редактирование шаблона разрешений
    :param request:
    :param preset_id:
    :return:
    """
    preset = get_object_or_404(PresetAccess, id=preset_id)
    if request.POST:
        formset_preset = FormPresetTitle(request.POST, instance=preset)
        if not PresetAccess.objects.filter(title=formset_preset['title'].value(), ).exclude(id=preset_id).exists():
            formset_preset.save()
            Access.objects.filter(preset=preset).delete()
            for permission in Permission.objects.all():
                access = request.POST.get(permission.name, False)
                if access:
                    Access(permission=permission, preset=preset, value=True).save()
            messages.success(request, 'Шаблон разрешений успешно сохранен.')
        else:
            messages.error(request, 'Шаблон разрешений с этим названием уже существует.')
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Шаблон разрешений ' + preset.title,
        'preset': preset,
        'form_preset_title': FormPresetTitle(initial={'title': preset.title}),
        'list_access': get_list_access(preset=preset),
    }
    return render(request=request, template_name='configure/preset_edit.html', context=context)


######################################################################################################################


@permission_required(['configure_edit', ])
def address_edit(request, address_id):
    """
    Редактирование адреса
    :param request:
    :param address_id:
    :return:
    """
    address = get_object_or_404(Address, id=address_id)
    if request.POST:
        formset = FormAddress(request.POST, instance=address)
        if formset.is_valid():
            formset.save()
            messages.info(request, 'Адрес {0} сохранен.'.format(address))
            return redirect(reverse('address_list'))
        else:
            messages.error(request, 'Ошибка при сохранении адреса {0}.'.format(address))
    else:
        formset = FormAddress(instance=address)
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Адрес {0}'.format(address),
        'url_breadcrumb': 'address_list',
        'title_breadcrumb': 'Список адресов',
        'url_delete': 'address_delete',
        'title_delete': 'Удалить адрес',
        'item': address,
        'formset': formset,
    }
    return render(request=request, template_name='configure/edit.html', context=context)


######################################################################################################################


@permission_required(['configure_edit', ])
def subnet_edit(request, subnet_id):
    """
    Редактирование подсети
    :param request:
    :param subnet_id:
    :return:
    """
    subnet = get_object_or_404(Subnet, id=subnet_id)
    if request.POST:
        formset = FormSubnet(request.POST, instance=subnet)
        if formset.is_valid():
            formset.save()
            messages.info(request, 'Подсеть {0} сохранена.'.format(subnet))
            return redirect(reverse('subnet_list'))
        else:
            messages.error(request, 'Ошибка при сохранении подсети {0}.'.format(subnet))
    else:
        formset = FormSubnet(instance=subnet)
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Подсеть {0}'.format(subnet),
        'url_breadcrumb': 'subnet_list',
        'title_breadcrumb': 'Список подсетей',
        'url_delete': 'subnet_delete',
        'title_delete': 'Удалить подсеть',
        'item': subnet,
        'formset': formset,
    }
    return render(request=request, template_name='configure/edit.html', context=context)


######################################################################################################################


@permission_required(['configure_edit', ])
def preset_delete(request, preset_id):
    """
    Удаление шаблона разрешений
    :param request:
    :param preset_id:
    :return:
    """
    preset = get_object_or_404(PresetAccess, id=preset_id)
    preset.delete()
    return redirect(reverse('preset_list'))


######################################################################################################################


@permission_required(['configure_edit', ])
def address_delete(request, address_id):
    """
    Удаление адреса
    :param request:
    :param address_id:
    :return:
    """
    address = get_object_or_404(Address, id=address_id)
    address.delete()
    return redirect(reverse('address_list'))


######################################################################################################################


@permission_required(['configure_edit', ])
def subnet_delete(request, subnet_id):
    """
    Удаление подсети
    :param request:
    :param subnet_id:
    :return:
    """
    subnet = get_object_or_404(Subnet, id=subnet_id)
    subnet.delete()
    return redirect(reverse('subnet_list'))


######################################################################################################################
