# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, Http404
from Main.tools import get_current_user
from datetime import datetime, timedelta
from uuid import uuid4
from Signature.models import Certificate
from Signature.forms import FormUpload
from Signature.certificate import Certificate as Cert
from Signature.choices import STATUS_CHOICES
from Signature.tools import get_signature, get_list_signature, change_status_signature, check_status_signature
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
            list_certificate.append((status, list_signature))
        list_current_signature = get_list_signature(current_user=current_user, status=0, all_organization=False)
        if check_status_signature(list_current_signature):
            list_current_signature = get_list_signature(current_user=current_user, status=0, all_organization=False)
        context = {
            'current_user': current_user,
            'title': 'Список электронных подписей',
            'form_upload': FormUpload(initial={'status': '0', }),
            'list_certificate': list_certificate,
            'date_warning': datetime.now().date() + timedelta(days=31),
            'date_danger': datetime.now().date() + timedelta(days=8),
            'list_current_signature': list_current_signature,
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
            file_signature = request.FILES['file_sign']
            signature_new = Certificate(
                owner=current_user,
                file_name=file_signature.name,
            )
            signature_new.file_sign.save(uuid4().hex, file_signature)
            if signature_new.parse_file():
                if request.POST.get('status', '0') == '1':
                    renew = request.POST.get('renew', '0')
                    if renew != '0':
                        signature_extended = get_object_or_404(Certificate, id=int(renew))
                        # TODO: сделать проверку на число
                        signature_new.renew = signature_extended
                        signature_extended.extended = signature_new
                        signature_extended.save()
                        # Статус равный 1 - Продлен
                        change_status_signature(signature_extended, status=1, file_delete=True)
                signature_new.save()
                return redirect(reverse('signature_show', args=(signature_new.id,)))
            else:
                signature_new.file_sign.delete()
                signature_new.delete()
                # TODO: return redirect(reverse('error'))
    return redirect(reverse('signature_list'))


######################################################################################################################


@login_required
def signature_show(request, signature_id):
    """
    Отображение выбранной электронной подписи
    :param request:
    :param signature_id:
    :return: render signature/show
    """
    signature = get_signature(request, signature_id=signature_id)
    if signature:
        current_user = get_current_user(request)
        context = {
            'current_user': current_user,
            'title': 'Сертификат электронной подписи',
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
def signature_terminate(request, signature_id) -> HttpResponse:
    """
    Смена статуса сертификата на Аннулирован и удаление файла электронной подписи
    :param request:
    :param signature_id:
    :return: HttpResponse
    """
    signature = get_signature(request, signature_id=signature_id)
    if signature:
        # Статус равный 3 - Аннулирован
        change_status_signature(signature, status=3, file_delete=True)
    return redirect(reverse('signature_show', args=(signature_id, )))


######################################################################################################################


@login_required
def signature_delete(request, signature_id):
    """
    Удаление сертификата и удаление файла электронной подписи
    :param request:
    :param signature_id:
    :return: redirect to signature_list
    """
    signature = get_signature(request, signature_id=signature_id)
    if signature:
        signature.file_sign.delete()
        signature.delete()
    return redirect(reverse('signature_list'))


######################################################################################################################


@login_required
def signature_file_download(request, signature_id):
    """
    Скачивание файла электронной подписи
    :param request:
    :param signature_id:
    :return: response or redirect to Http404
    """
    signature = get_signature(request, signature_id=signature_id)
    if signature:
        response = HttpResponse(signature.file_sign.file)
        file_type = mimetypes.guess_type(signature.file_sign.name)
        if file_type is None:
            file_type = 'application/octet-stream'
        response['Content-Type'] = file_type
        response['Content-Length'] = signature.file_sign.size
        response['Content-Disposition'] = "attachment; filename="+signature.file_name
        return response
    raise Http404


######################################################################################################################
