# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from Main.tools import get_current_user
from .models import Certificate
from .choices import STATUS_CHOICES

######################################################################################################################


def get_esign(request, esign_id):
    """
    Получение элемента Сертификат, с проверкой прав на чтение данного элемента
    :param request:
    :param esign_id:
    :return:
    """
    current_user = get_current_user(request)
    esign = get_object_or_404(Certificate, id=esign_id)
    if current_user.access.esign_edit and esign.owner.organization == current_user.organization:
        return esign
    else:
        return None


######################################################################################################################


def get_list_esign(current_user, status=0, all_organization=False):
    """
    Получение списка Сертификатов с определенным статусом
    :param current_user:
    :param status:
    :param all:
    :return:
    """
    if all_organization and current_user.access.esign_moderator:
        esign_list = Certificate.objects.filter(
            status=status
        )
    else:
        esign_list = Certificate.objects.filter(
            status=status,
            owner__organization=current_user.organization
        )
    return esign_list

######################################################################################################################


def get_count_esign(current_user):
    """
    Получение количества сертификатов, в зависимости от статуса
    :param current_user:
    :return:
    """
    esign_count_list = []
    for status in STATUS_CHOICES:
        if current_user.access.esign_moderator:
            esign_count = Certificate.objects.filter(
                status=status[0]
            ).count()
        else:
            esign_count = Certificate.objects.filter(
                status=status[0],
                owner__organization=current_user.organization
            ).count()
        esign_count_list.append((status[0], status[1], esign_count))
    return esign_count_list


######################################################################################################################


def get_esign_expires_count(current_user):
    """
    Подсчет сертификатов со сроком истечения менее 30 дней
    :param current_user:
    :return:
    """
    if current_user.access.esign_moderator:
        esign_expires_count = Certificate.objects.filter(
            status=0,
            valid_for__lte=datetime.now().date() + timedelta(days=30)
        ).count()
    else:
        esign_expires_count = Certificate.objects.filter(
            status=0,
            valid_for__lte=datetime.now().date() + timedelta(days=30),
            owner__organization=current_user.organization
        ).count()
    return esign_expires_count

######################################################################################################################


def change_status_esign(esign: Certificate, status=0, file_delete=False) -> None:
    """
    Процедура по смене статуса сертификата
    :param esign:
    :param status:
    :param file_delete:
    :return: None
    """
    if isinstance(status, int):
        esign.status = status
        if file_delete:
            esign.file_name = ''
            esign.file_sign.delete()
        esign.save()


######################################################################################################################


def check_status_esign(esign_list) -> bool:
    """
    Процедура проверкти сертификата на актуальность и смена статуса, в зависимости от текущей даты
    :param esign_list:
    :return:
    """
    change = False
    for esign in esign_list:
        if esign.valid_for.date() < datetime.now().date():
            change_status_esign(esign, status=2, file_delete=True)
            change = True
    return change


######################################################################################################################
