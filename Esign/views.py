# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from Profile.models import UserProfile
from Esign.models import Certificate
from Esign.forms import FormUpload
from Main.decorators import access_esign_list, access_esign_edit
from datetime import datetime, timedelta
import fsb795
import mimetypes

######################################################################################################################


def esign_check_current(esign_list):
    current_date = datetime.now().date()
    for esign in esign_list:
        esign_date = esign.valid_for.date()
        if esign_date < (current_date + timedelta(days=30)):
            esign.is_expires = True
            if esign_date < current_date:
                esign.is_current = False
            esign.save()


######################################################################################################################


@login_required
@access_esign_list
def esign_get_list(request):
    # Список электронных подписей
    current_user = get_object_or_404(UserProfile, user=request.user)
    if request.POST and request.FILES:
        esign = Certificate()
        esign.owner = current_user
        file = request.FILES['file']
        esign.file_sign.save(file.name, file)
        cert = fsb795.Certificate(esign.file_sign.path)
        if cert.pyver == '':
            esign.file_sign.delete()
            esign.delete()
        else:
            iss, vlad_is = cert.issuerCert()
            esign.issuer = iss['CN']
            sub, vlad_sub = cert.subjectCert()
            esign.entity = sub['CN']
            serial = str(hex(cert.serialNumber()))
            # Убираем из серийного номера символ (x) - обозначение шестнадцатеричной строки
            serial = serial[0] + serial[2:]
            esign.serial = serial
            valid = cert.validityCert()
            esign.valid_from = valid['not_before']
            esign.valid_for = valid['not_after']
            if request.POST.get('select', '0') == '1':
                renew = request.POST.get('renew', '0')
                if renew != '0':
                    esign_extended = get_object_or_404(Certificate, id=int(renew))
                    esign.renew = esign_extended
                    esign.save()
                    esign_extended.is_extended = True
                    esign_extended.is_current = False
                    esign_extended.extended = esign
                    esign_extended.save()
            esign.save()
        return redirect(reverse('esign_list'))
    else:
        if current_user.access.esign_moderator:
            esign_check_current(list(Certificate.objects.filter(is_current=True)))
            esign_list_current = Certificate.objects.filter(is_current=True)
            esign_list_expires = Certificate.objects.filter(is_expires=True)
            esign_list_extended = Certificate.objects.filter(is_extended=True)
            esign_list_terminate = Certificate.objects.filter(is_terminate=True)
        else:
            esign_check_current(list(Certificate.objects.filter(is_current=True).filter(owner__organization=current_user.organization)))
            esign_list_current = Certificate.objects.filter(is_current=True).filter(owner__organization=current_user.organization)
            esign_list_expires = Certificate.objects.filter(is_expires=True).filter(owner__organization=current_user.organization)
            esign_list_extended = Certificate.objects.filter(is_extended=True).filter(owner__organization=current_user.organization)
            esign_list_terminate = Certificate.objects.filter(is_terminate=True).filter(owner__organization=current_user.organization)
        context = {
            'current_user': current_user,
            'form_upload': FormUpload(),
            'esign_list_current': esign_list_current,
            'esign_list_expires': esign_list_expires,
            'esign_list_extended': esign_list_extended,
            'esign_list_terminate': esign_list_terminate,
            'esign_count_current': esign_list_current.count(),
            'esign_count_expires': esign_list_expires.count(),
            'esign_count_extended': esign_list_extended.count(),
            'esign_count_terminate': esign_list_terminate.count(),
        }
        return render(request, 'esign/list.html', context)


######################################################################################################################


@login_required
@access_esign_edit
def esign_show(request, esign_id):
    # Список электронных подписей
    current_user = get_object_or_404(UserProfile, user=request.user)
    esign = get_object_or_404(Certificate, id=esign_id)
    context = {
        'current_user': current_user,
        'esign': esign,
    }
    cert = fsb795.Certificate(esign.file_sign.path)
    if cert.pyver != '':
        iss, vlad_is = cert.issuerCert()
        sub, vlad_sub = cert.subjectCert()
        context['iss'] = iss
        context['sub'] = sub
    return render(request, 'esign/show.html', context)


######################################################################################################################


@login_required
@access_esign_edit
def esign_terminate(request, esign_id):
    # Смена статуса сертификата на Аннулирован
    esign = get_object_or_404(Certificate, id=esign_id)
    esign.is_current = False
    esign.is_terminate = True
    esign.save()
    return redirect(reverse('esign_show', args=(esign_id, )))


######################################################################################################################


@login_required
@access_esign_edit
def esign_download(request, esign_id):
    # Смена статуса сертификата на Аннулирован
    esign = get_object_or_404(Certificate, id=esign_id)
    response = HttpResponse(esign.file_sign.file)
    file_type = mimetypes.guess_type(esign.file_sign.name)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = esign.file_sign.size
    response['Content-Disposition'] = "attachment; filename=" + esign.file_sign.name
    return response


######################################################################################################################
