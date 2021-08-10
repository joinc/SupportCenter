# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
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
        print(request.FILES.getlist('files'), )
        contract = Contract()
        formset_contract = FormContract(request.POST, instance=contract)
        if formset_contract.is_valid():
            formset_contract.save()
            if first_status:
                if change_stage(request=request, contract=contract, current_status=first_status):
                    messages.success(request, 'Контракт {0} успешно создан.'.format(contract.title))
                else:
                    messages.error(request, 'Ошибка при создании контракта.1')
            else:
                messages.error(request, 'Не заданы стадии.')
            return redirect(reverse('contract_show', args=(contract.id, )))
        else:
            messages.error(request, 'Ошибка при создании контракта.2')
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

    # from django.http import HttpResponse, Http404

    # signature = get_signature(request, signature_id=signature_id)
    # if signature:
    #     response = HttpResponse(signature.file_sign.file)
    #     file_type = mimetypes.guess_type(signature.file_sign.name)
    #     if file_type is None:
    #         file_type = 'application/octet-stream'
    #     response['Content-Type'] = file_type
    #     response['Content-Length'] = signature.file_sign.size
    #     response['Content-Disposition'] = "attachment; filename="+signature.file_name
    #     return response
    # raise Http404

######################################################################################################################
