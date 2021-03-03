# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from Signature.models import Certificate
from Main.tools import get_profile
from Main.choices import STATUS_SIGNATURE_CHOICES

######################################################################################################################


def get_signature(request, signature_id) -> Certificate or None:
    """
    Получение элемента Сертификат, с проверкой прав на чтение данного элемента
    :param request:
    :param signature_id:
    :return:
    """
    current_user = get_profile(user=request.user)
    signature = get_object_or_404(Certificate, id=signature_id)
    if current_user.access(list_permission=['signature_edit', ]) \
            and signature.owner.organization == current_user.organization:
        return signature
    else:
        return None


######################################################################################################################


def get_list_signature(current_user, status=0, all_organization=False) -> list:
    """
    Получение списка Сертификатов с определенным статусом
    :param current_user:
    :param status:
    :param all_organization:
    :return:
    """
    if all_organization and current_user.access(list_permission=['signature_moderator', ]):
        list_signature = Certificate.objects.filter(
            status=status,
        )
    else:
        list_signature = Certificate.objects.filter(
            status=status,
            owner__organization=current_user.organization
        )
    return list_signature


######################################################################################################################


def get_count_signature(current_user) -> list:
    """
    Получение количества сертификатов, в зависимости от статуса
    :param current_user:
    :return:
    """
    list_count_signature = []
    for status in STATUS_SIGNATURE_CHOICES:
        if current_user.access(list_permission=['signature_moderator', ]):
            count = Certificate.objects.filter(
                status=status[0],
            ).count()
        else:
            count = Certificate.objects.filter(
                status=status[0],
                owner__organization=current_user.organization,
            ).count()
        list_count_signature.append((status, count))
    return list_count_signature


######################################################################################################################


def get_count_expires_signature(current_user) -> int:
    """
    Подсчет сертификатов со сроком истечения менее 30 дней
    :param current_user:
    :return:
    """
    if current_user.access(list_permission=['signature_moderator', ]):
        count_expires_signature = Certificate.objects.filter(
            status=0,
            valid_for__lte=datetime.now().date() + timedelta(days=30),
        ).count()
    else:
        count_expires_signature = Certificate.objects.filter(
            status=0,
            valid_for__lte=datetime.now().date() + timedelta(days=30),
            owner__organization=current_user.organization,
        ).count()
    return count_expires_signature


######################################################################################################################


def change_status_signature(signature: Certificate, status=0, file_delete=False) -> bool:
    """
    Процедура по смене статуса сертификата
    :param signature:
    :param status:
    :param file_delete:
    :return: bool
    """
    if isinstance(status, int):
        signature.status = status
        if file_delete:
            signature.file_name = ''
            signature.file_sign.delete()
        signature.save()
        return True
    return False


######################################################################################################################


def check_status_signature(list_signature) -> bool:
    """
    Процедура проверкти сертификата на актуальность и смена статуса, в зависимости от текущей даты
    :param list_signature:
    :return: bool
    """
    change = False
    for signature in list_signature:
        if signature.valid_for.date() < datetime.now().date():
            change_status_signature(signature, status=2, file_delete=True)
            change = True
    return change


######################################################################################################################
