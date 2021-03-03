# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ipaddress import IPv4Address, IPv4Network
from Violation.models import Incident, Violator, ReportViolation, FileViolation
from Violation.forms import FormViolation
from Workplace.models import Subnet
from Organization.models import OrganizationSubnet
from Main.decorators import permission_required
from Main.tools import get_profile
import csv

######################################################################################################################


@permission_required(['violation_list', 'violation_edit', 'violation_moderator', ])
def violation_list(request):
    """
    Список отчетов об инцидентах
    :param request:
    :return: HttpResponse
    """
    current_user = get_profile(user=request.user)
    context = {
        'current_user': current_user,
        'title': 'Список отчетов об инцидентах',
        'list_violation': ReportViolation.objects.all(),
        'violation_moderator': current_user.access(list_permission=['violation_moderator', ])
    }
    return render(request=request, template_name='violation/list.html', context=context)


######################################################################################################################

def violation_create(report_violation):
    """
    Загрузка отчета об инцидентах
    :param report_violation:
    :return:
    """
    list_file_violation = FileViolation.objects.filter(violation=report_violation)
    if list_file_violation:
        start_time = datetime.now()
        for file_violation in list_file_violation:
            with open(file_violation.file.path) as csv_file:
                count = 0
                reader = csv.reader(csv_file, delimiter=';')
                for index, row in enumerate(list(reader)):
                    if index > 0:
                        if not Incident.objects.filter(id_ids=row[0]).exists():
                            count = index + 1
                            violator, create = Violator.objects.get_or_create(
                                violation=report_violation,
                                ip_violator=row[5],
                            )
                            if create:
                                for subnet in Subnet.objects.all():
                                    if IPv4Address(violator.ip_violator) in IPv4Network(subnet.subnet):
                                        violator.subnet = subnet
                                        violator.save(update_fields=['subnet'])
                            Incident(
                                violator=violator,
                                id_ids=row[0],
                                time_stamp=row[1],
                                code_incident=row[2],
                                aggregated=row[3],
                                aggregation_period=row[4],
                                source_ip=row[5],
                                source_port=row[6],
                                source_MAC=row[7],
                                destination_ip=row[8],
                                destination_port=row[9],
                                destination_MAC=row[10],
                                protocol=row[11],
                                protocol_name=row[12],
                                class_incident=row[13],
                                message_incident=row[14],
                                priority=row[15],
                            ).save()
        delta_time = datetime.now() - start_time
        print('Потрачено времени {0} для внесения {1} инцидентов.'.format(delta_time, count))
        return True
    return False


######################################################################################################################


@permission_required(['violation_moderator', ])
def violation_load(request):
    """
    Загрузка отчета о нарушениях
    :param request:
    :return:
    """
    if request.POST:
        report_violation = ReportViolation()
        formset = FormViolation(request.POST, request.FILES, instance=report_violation)
        if formset.is_valid():
            formset.save()
            for file in request.FILES.getlist('files'):
                file_violation = FileViolation(violation=report_violation, )
                file_violation.file.save(file.name, file)
                file_violation.save()
            if violation_create(report_violation=report_violation):
                messages.success(request, 'Отчет {0} успешно загружен.'.format(report_violation))
                return redirect(reverse('violation_list'))
            else:
                messages.error(request, 'Ошибка при загрузке файлов отчета')
        else:
            messages.error(request, 'Ошибка при загрузке отчета. Форма заполнена не корректно.')
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Загрузка инцидентов',
        'form_violation': FormViolation(),
    }
    return render(request=request, template_name='violation/load.html', context=context)


######################################################################################################################


@login_required
def violation_show(request, violation_id):
    """
    Список нарушителей в отчете об инцидентах
    :param request:
    :param violation_id:
    :return:
    """
    violation = get_object_or_404(ReportViolation, id=violation_id)
    list_violator = []
    for violator in Violator.objects.filter(violation=violation):
        list_violator.append([violator, OrganizationSubnet.objects.filter(subnet=violator.subnet)])
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Отчет об инцидентах за ' + violation.date_violation.strftime('%d.%m.%Y'),
        'list_violator': list_violator,
    }
    return render(request=request, template_name='violation/show.html', context=context)


######################################################################################################################


@login_required
def violator_show(request, violator_id):
    """
    Список нарушителей в отчете об инцидентах
    :param request:
    :param violator_id:
    :return:
    """
    violator = get_object_or_404(Violator, id=violator_id)
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Отчет об инцидентах узла ' + violator.ip_violator,
        'violator': violator,
        'list_incident': Incident.objects.filter(violator=violator),
    }

    return render(request=request, template_name='violation/incident.html', context=context)


######################################################################################################################
