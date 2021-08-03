# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from Main.decorators import permission_required
from Main.tools import get_profile
from Contract.models import Contract
from Contract.forms import FormContract

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
    if request.POST:
        contract = Contract()
        formset = FormContract(request.POST, instance=contract)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Контракт {0} успешно создан.'.format(contract.title))
            # return redirect(reverse('contract_show', args=(contract.id, )))
            return redirect(reverse('contract_list'))
        else:
            messages.error(request, 'Ошибка при создании контракта.')
            return redirect(reverse('contract_list'))
    else:
        context = {
            'current_user': get_profile(user=request.user),
            'title': 'Добавление контракта',
            'form_contract': FormContract(),
        }
        return render(request=request, template_name='contract/create.html', context=context)


######################################################################################################################


@permission_required(['contract_list', 'contract_edit', 'contract_moderator', ])
def contract_show(request, contract_id):
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Добавление контракта',
        'contract': get_object_or_404(Contract, id=contract_id),
    }
    return render(request=request, template_name='contract/create.html', context=context)
