# -*- coding: utf-8 -*-

from django.contrib import messages
from uuid import uuid4
from Contract.models import Stage, Attache
from Contract.forms import FormStage

######################################################################################################################


def change_stage(request, contract, current_status):
    stage = Stage(contract=contract, status=current_status)
    formset_stage = FormStage(request.POST, request.FILES, instance=stage)
    if formset_stage.is_valid():
        formset_stage.save()
        for file_attache in request.FILES.getlist('files'):
            attache = Attache(name=file_attache.name, stage=stage)
            attache.file.save(uuid4().hex, file_attache)
            attache.save()
            if not current_status.next_status:
                contract.closed = True
                contract.save()
        return True
    else:
        messages.error(request, 'Ошибка при создании стадии контракта.')
        return False


######################################################################################################################
