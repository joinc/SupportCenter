# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, reverse
from Main.tools import get_current_user
from Main.forms import FormPresetTitle
from Profile.models import PresetAccess, CategoryPermission, Permission, Access

######################################################################################################################


@login_required
def configure_list(request):
    """
    Отображение списка настроек
    :param request:
    :return: HttpResponse
    """
    if request.user.is_superuser:
        list_configure = {
            'Профиль пользователя': {
                'Список шаблонов разрешений': reverse('preset_list'),
                'Настройка 2': reverse('index'),
                'Настройка 3': reverse('index'),
            },
            'Модуль 2': {
                'Настройка 1': reverse('index'),
                'Настройка 2': reverse('index'),
                'Настройка 3': reverse('index'),
            },
            'Модуль 3': {
                'Настройка 1': reverse('index'),
                'Настройка 2': reverse('index'),
                'Настройка 3': reverse('index'),
            },
        }
        context = {
            'current_user': get_current_user(user=request.user),
            'title': 'Список конфигураций',
            'list_configure': list_configure,
        }
        return render(request=request, template_name='configure/list.html', context=context)
    return redirect(reverse('index'))


######################################################################################################################


def preset_create(request):
    """
    Создание нового шаблона разрешений
    :param request:
    :return:
    """
    if request.POST:
        formset = FormPresetTitle(request.POST)
        title = formset['title'].value()
        if title:
            preset, create = PresetAccess.objects.get_or_create(title=title)
            if create:
                preset.is_sample = True
                preset.save()
                return redirect(reverse('preset_edit', args=(preset.id,)))
            else:
                messages.info(request, 'Шаблон разрешений с этим названием уже существует.')
        else:
            messages.info(request, 'Укажите название шаблона разрешений.')
    else:
        formset = FormPresetTitle()
    context = {
        'current_user': get_current_user(user=request.user),
        'title': 'Создание шаблона разрешений',
        'form_preset_title': formset,
    }
    return render(request=request, template_name='configure/preset_create.html', context=context)


######################################################################################################################


def preset_list(request):
    """
    Отображение списка шаблоново разрешений
    :param request:
    :return:
    """
    context = {
        'current_user': get_current_user(user=request.user),
        'title': 'Список шаблонов разрешений',
        'list_preset': PresetAccess.objects.filter(is_sample=True, )
    }
    return render(request=request, template_name='configure/preset_list.html', context=context)


######################################################################################################################


def get_list_access(preset):
    list_access = []
    for category in CategoryPermission.objects.all():
        list_permission = []
        for permission in Permission.objects.filter(category=category):
            if Access.objects.filter(permission=permission, preset=preset).exists():
                list_permission.append([
                    permission.title,
                    permission.name,
                    Access.objects.get(permission=permission, preset=preset).value,
                ])
            else:
                list_permission.append([
                    permission.title,
                    permission.name,
                    False,
                ])
        list_access.append([category, list_permission])
    return list_access


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
        'current_user': get_current_user(user=request.user),
        'title': 'Шаблон разрешений ' + preset.title,
        'preset': preset,
        'form_preset_title': FormPresetTitle(initial={'title': preset.title}),
        'list_access': get_list_access(preset=preset),
    }
    return render(request=request, template_name='configure/preset_edit.html', context=context)


######################################################################################################################


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
