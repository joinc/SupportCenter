# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from Profile.models import UserProfile
from Esign.models import Certificate
from Esign.forms import FormUpload
from Main.decorators import access_esign_list, access_esign_edit
import fsb795

######################################################################################################################


@login_required
@access_esign_list
def esign_list(request):
    # Список электронных подписей
    current_user = get_object_or_404(UserProfile, user=request.user)
    if current_user.access.esign_moderator:
        # esign_list = Certificate.objects.filter(is_terminate=False)
        esign_list = Certificate.objects.all()
    else:
        # esign_list = Certificate.objects.filter(owner__organization=current_user.organization).filter(is_terminate=False)
        esign_list = Certificate.objects.filter(owner__organization=current_user.organization)
    context = {
        'current_user': current_user,
        'form_upload': FormUpload(),
        'esign_total': len(esign_list),
        'esign_list': esign_list,
        'renew_list': list(
            map(
                lambda x: [x['id'], x['entity'], x['valid_from'], x['valid_for']],
                list(
                    Certificate.objects.values(
                        'id',
                        'entity',
                        'valid_from',
                        'valid_for',
                    ).filter(
                        is_terminate=False
                    ).filter(
                        is_extended=False
                    ).filter(
                        owner__organization=current_user.organization
                    )
                )
            )
        ),
    }
    if request.POST and request.FILES:
        esign = Certificate()
        esign.owner = current_user
        file = request.FILES['file']
        esign.file_sign.save(file.name, file)
        cert = fsb795.Certificate(esign.file_sign.path)
        if cert.pyver == '':
            esign.delete()
            return redirect(reverse('esign_list'))
        iss, vlad_is = cert.issuerCert()
        esign.issuer = iss['CN']
        sub, vlad_sub = cert.subjectCert()
        esign.entity = sub['CN']
        serial = str(hex(cert.serialNumber()))
        serial = serial[0] + serial[2:]
        esign.serial = serial
        valid = cert.validityCert()
        esign.valid_from = valid['not_before']
        esign.valid_for = valid['not_after']
        if request.POST.get('status', '0') == '1':
            renew = request.POST.get('renew', '0')
            if renew != '0':
                esign_extended = get_object_or_404(Certificate, id=int(renew))
                esign.renew = esign_extended
                esign.save()
                esign_extended.is_extended = True
                esign_extended.extended = esign
                esign_extended.save()
        esign.save()
        return redirect(reverse('esign_list'))
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
    esign.is_terminate = True
    esign.save()
    return redirect(reverse('esign_show', args=(esign_id, )))


######################################################################################################################


@login_required
@access_esign_edit
def esign_download(request, esign_id):
    # Смена статуса сертификата на Аннулирован
    esign = get_object_or_404(Certificate, id=esign_id)
    return redirect(reverse('esign_list'))
######################################################################################################################
