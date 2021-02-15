# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, Http404
from Main.tools import get_current_user
from datetime import datetime, timedelta
from uuid import uuid4
from .models import Certificate
from .forms import FormUpload
from .certificate import Certificate as Cert
from .choices import STATUS_CHOICES
from .tools import get_signature, get_list_signature, change_status_signature, check_status_signature
import mimetypes

######################################################################################################################


@login_required
def signature_list(request):
    """
    Список электронных подписей
    :param request:
    :return: render signature/list
    """
    current_user = get_current_user(request)
    if current_user.access.signature_list:
        list_certificate = []
        for status in STATUS_CHOICES:
            list_signature = get_list_signature(current_user=current_user, status=status[0], all_organization=True)
            list_certificate.append((status[0], status[1], list_signature))
        list_current_esign = get_list_signature(current_user=current_user, status=0, all_organization=False)
        if check_status_signature(list_current_esign):
            list_current_esign = get_list_signature(current_user=current_user, status=0, all_organization=False)
        context = {
            'current_user': current_user,
            'title': 'Список электронных подписей',
            'form_upload': FormUpload(),
            'list_certificate': list_certificate,
            'date_warning': datetime.now().date() + timedelta(days=31),
            'date_danger': datetime.now().date() + timedelta(days=8),
            'list_current_signature': list_current_esign,
        }
        return render(request, 'signature/list.html', context)
    else:
        return redirect(reverse('index'))


######################################################################################################################


@login_required
def signature_file_upload(request):
    """
    Загрузка файла электронной подписи и создание записи в базе данной
    :param request:
    :return: redirect to signature_list
    """
    current_user = get_current_user(request)
    if current_user.access.esign_edit:
        if request.POST and request.FILES:
            esign_new = Certificate(owner=current_user)
            file = request.FILES['file']
            esign_new.file_name = request.FILES['file'].name
            esign_new.file_sign.save(uuid4().hex, file)
            if esign_new.parse_file():
                if request.POST.get('select', '0') == '1':
                    renew = request.POST.get('renew', '0')
                    if renew != '0':
                        esign_extended = get_object_or_404(Certificate, id=int(renew))
                        esign_new.renew = esign_extended
                        esign_extended.extended = esign_new
                        esign_extended.save()
                        # Статус равный 1 - Продлен
                        change_status_signature(esign_extended, status=1, file_delete=True)
                esign_new.save()
                return redirect(reverse('esign_show', args=(esign_new.id,)))
            else:
                esign_new.file_sign.delete()
                esign_new.delete()
                # TODO: return redirect(reverse('error'))
    return redirect(reverse('esign_list'))


######################################################################################################################


@login_required
def signature_show(request, signature_id):
    """
    Отображение выбранной электронной подписи
    :param request:
    :param signature_id:
    :return: render signature/show
    """
    signature = get_signature(request, esign_id=signature_id)
    if signature:
        current_user = get_current_user(request)
        context = {
            'current_user': current_user,
            'signature': signature,
        }
        if signature.file_sign:
            certificate = Cert(signature.file_sign.path)
            if certificate.cert_format:
                iss, vlad_is = certificate.issuerCert()
                sub, vlad_sub = certificate.subjectCert()
                context['iss'] = iss
                context['sub'] = sub
        return render(request, 'signature/show.html', context)
    else:
        return redirect(reverse('signature_list'))


######################################################################################################################


@login_required
def esign_terminate(request, signature_id):
    """
    Смена статуса сертификата на Аннулирован и удаление файла электронной подписи
    :param request:
    :param signature_id:
    :return: redirect to signature_show
    """
    signature = get_signature(request, esign_id=signature_id)
    if signature:
        # Статус равный 3 - Аннулирован
        change_status_signature(esign, status=3, file_delete=True)
    return redirect(reverse('esign_show', args=(esign_id, )))


######################################################################################################################


@login_required
def esign_delete(request, esign_id):
    """
    Удаление сертификата и удаление файла электронной подписи
    :param request:
    :param esign_id:
    :return: redirect to esign_list
    """
    esign = get_signature(request, esign_id=esign_id)
    if esign:
        esign.file_sign.delete()
        esign.delete()
    return redirect(reverse('esign_list'))


######################################################################################################################


@login_required
def esign_file_download(request, esign_id):
    """
    Скачивание файла электронной подписи
    :param request:
    :param esign_id:
    :return: response or redirect to Http404
    """
    esign = get_signature(request, esign_id=esign_id)
    if esign:
        response = HttpResponse(esign.file_sign.file)
        file_type = mimetypes.guess_type(esign.file_sign.name)
        if file_type is None:
            file_type = 'application/octet-stream'
        response['Content-Type'] = file_type
        response['Content-Length'] = esign.file_sign.size
        response['Content-Disposition'] = "attachment; filename="+esign.file_name
        return response
    raise Http404


######################################################################################################################
