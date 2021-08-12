# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, Http404
from django.contrib import messages
from transliterate import translit
from Main.decorators import permission_required
from Main.tools import get_profile
from Contract.models import Contract, Status, Stage, Attache
from Contract.forms import FormContract, FormStage
from Contract.tools import change_stage
import mimetypes

######################################################################################################################


@permission_required(['contract_list', 'contract_edit', 'contract_moderator', ])
def contract_list(request):
    """
    Вывод списка контрактов
    :param request:
    :return:
    """
    current_user = get_profile(user=request.user)
    context = {
        'current_user': current_user,
        'title': 'Список контрактов',
        'access_edit': current_user.access(list_permission=['contract_edit', ]),
        'list_contract': Contract.objects.all(),
    }
    return render(request=request, template_name='contract/list.html', context=context)


######################################################################################################################


@permission_required(['contract_edit', ])
def contract_create(request):
    """
    СОздание нового контракта
    :param request:
    :return:
    """
    first_status = Status.objects.first()
    if request.POST and request.FILES:
        contract = Contract()
        formset_contract = FormContract(request.POST, instance=contract)
        if formset_contract.is_valid():
            formset_contract.save()
            if first_status:
                if change_stage(request=request, contract=contract, status=first_status):
                    messages.success(request, 'Контракт {0} успешно создан.'.format(contract.title))
                else:
                    messages.error(request, 'Ошибка при создании стадии контракта.')
            else:
                messages.error(request, 'Не заданы стадии.')
            return redirect(reverse('contract_show', args=(contract.id, )))
        else:
            messages.error(request, 'Ошибка при создании контракта.')
            return redirect(reverse('contract_create'))
    else:
        context = {
            'current_user': get_profile(user=request.user),
            'title': 'Добавление контракта',
            'list_breadcrumb': (
                (reverse('contract_list'), 'Список контрактов'),
            ),
            'first_status': first_status,
            'form_contract': FormContract(),
            'form_stage': FormStage(),
        }
        return render(request=request, template_name='contract/create.html', context=context)


######################################################################################################################


@permission_required(['contract_list', 'contract_edit', 'contract_moderator', ])
def contract_show(request, contract_id):
    """
    Просмотр контракта
    :param request:
    :param contract_id:
    :return:
    """
    contract = get_object_or_404(Contract, id=contract_id)
    list_stage = []
    stages = Stage.objects.filter(contract=contract)
    for stage in stages:
        list_attach = list(Attache.objects.filter(stage=stage))
        list_stage.append([stage, list_attach])
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Контракт {0}'.format(contract.title),
        'list_breadcrumb': (
            (reverse('contract_list'), 'Список контрактов'),
        ),
        'contract': contract,
        'list_stage': list_stage,
        'current_stage': Stage.objects.filter(contract=contract).last(),
        'form_stage': FormStage(),
    }
    return render(request=request, template_name='contract/show.html', context=context)


######################################################################################################################


@permission_required(['contract_list', 'contract_edit', 'contract_moderator', ])
def attache_download(request, attache_id):
    """
    Скачивание приложения стадии контракта
    :param request:
    :param attache_id:
    :return:
    """
    if request.POST:
        attache = get_object_or_404(Attache, id=attache_id)
        response = HttpResponse(attache.file)
        file_type = mimetypes.guess_type(attache.name)
        if file_type is None:
            file_type = 'application/octet-stream'
        response['Content-Type'] = file_type
        response['Content-Length'] = attache.file.size
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            translit(attache.name, language_code='ru', reversed=True)
        )
        return response
    else:
        raise Http404


######################################################################################################################


@permission_required(['contract_list', 'contract_edit', 'contract_moderator', ])
def add_stage(request, contract_id):
    """
    Добавление новой стадии контракта
    :param request:
    :param contract_id:
    :return:
    """
    if request.POST:
        contract = get_object_or_404(Contract, id=contract_id)
        current_stage = Stage.objects.filter(contract=contract).last()
        if current_stage.status.next_status:
            if change_stage(request=request, contract=contract, status=current_stage.status.next_status):
                messages.success(request, 'Стадия контракта успешно добавлена.')
            else:
                messages.error(request, 'Ошибка при создании стадии контракта.')
        else:
            messages.error(request, 'Отсутвует следующая стадия контракта.')
        return redirect(reverse('contract_show', args=(contract.id,)))
    else:
        raise Http404


######################################################################################################################
