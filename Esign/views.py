# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, Http404
from Main.tools import get_current_user
from datetime import datetime, timedelta
from uuid import uuid4
from .models import Certificate
from .forms import FormUpload
from .certificate import Certificate as cert
from .choices import STATUS_CHOICES
from .tools import get_esign, get_list_esign, change_status_esign, check_status_esign
import mimetypes

######################################################################################################################


@login_required
def esign_list(request):
    """
    Список электронных подписей
    :param request:
    :return: render esign/list
    """
    current_user = get_current_user(request)
    if current_user.access.esign_list:
        list_cert = []
        for status in STATUS_CHOICES:
            list_esign = get_list_esign(current_user=current_user, status=status[0], all_organization=True)
            list_cert.append((status[0], status[1], list_esign))
        list_current_esign = get_list_esign(current_user=current_user, status=0, all_organization=False)
        if check_status_esign(list_current_esign):
            list_current_esign = get_list_esign(current_user=current_user, status=0, all_organization=False)
        context = {
            'current_user': current_user,
            'form_upload': FormUpload(),
            'list_cert': list_cert,
            'date_warning': datetime.now().date() + timedelta(days=31),
            'date_danger': datetime.now().date() + timedelta(days=8),
            'list_current_esign': list_current_esign,
        }
        return render(request, 'esign/list.html', context)
    else:
        return redirect(reverse('index'))


######################################################################################################################


@login_required
def esign_file_upload(request):
    """
    Загрузка файла электронной подписи и создание записи в базе данной
    :param request:
    :return: redirect to esign_list
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
                        change_status_esign(esign_extended, status=1, file_delete=True)
                esign_new.save()
                return redirect(reverse('esign_show', args=(esign_new.id,)))
            else:
                esign_new.file_sign.delete()
                esign_new.delete()
                # TODO: return redirect(reverse('error'))
    return redirect(reverse('esign_list'))


######################################################################################################################


@login_required
def esign_show(request, esign_id):
    """
    Отображение выбранной электронной подписи
    :param request:
    :param esign_id:
    :return: render esign/show
    """
    esign = get_esign(request, esign_id=esign_id)
    if esign:
        current_user = get_current_user(request)
        context = {
            'current_user': current_user,
            'esign': esign,
        }
        if esign.file_sign:
            certificate = cert(esign.file_sign.path)
            if certificate.cert_format:
                iss, vlad_is = certificate.issuerCert()
                sub, vlad_sub = certificate.subjectCert()
                context['iss'] = iss
                context['sub'] = sub
        return render(request, 'esign/show.html', context)
    else:
        return redirect(reverse('esign_list'))


######################################################################################################################


@login_required
def esign_terminate(request, esign_id):
    """
    Смена статуса сертификата на Аннулирован и удаление файла электронной подписи
    :param request:
    :param esign_id:
    :return: redirect to esign_show
    """
    esign = get_esign(request, esign_id=esign_id)
    if esign:
        # Статус равный 3 - Аннулирован
        change_status_esign(esign, status=3, file_delete=True)
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
    esign = get_esign(request, esign_id=esign_id)
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
    esign = get_esign(request, esign_id=esign_id)
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
