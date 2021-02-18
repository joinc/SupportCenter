# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ipaddress import IPv4Address, IPv4Network
from Violation.models import Incident, Violator, ReportViolation
from Workplace.models import Subnet
from Organization.models import SubnetOrg
from Violation.forms import FormViolation
from Main.tools import get_current_user
import csv

######################################################################################################################


@login_required
def violation_load(request):
    """
    Загрузка отчета о нарушениях
    :param request:
    :return:
    """
    context = {
        'current_user': get_current_user(user=request.user),
        'title': 'Загрузка инцидентов',
        'form_violation': FormViolation(),
    }
    return render(request, 'violation/load.html', context)


######################################################################################################################


@login_required
def violation_create(request):
    """
    Загрузка отчета об инцидентах
    :param request:
    :return:
    """
    if request.POST:
        formset = FormViolation(request.POST, request.FILES)
        if formset.is_valid():
            violation = formset.save()
            start_time = datetime.now()
            with open(violation.file_violation.path) as csv_file:
                count = 0
                reader = csv.reader(csv_file, delimiter=';')
                for index, row in enumerate(list(reader)):
                    if index > 0:
                        if not Incident.objects.filter(id_ids=row[0]).exists():
                            count = index + 1
                            violator, create = Violator.objects.get_or_create(
                                violation=violation,
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
    return redirect(reverse('violation_list'))


######################################################################################################################


@login_required
def violation_list(request):
    """
    Список отчетов об инцидентах
    :param request:
    :return: HttpResponse
    """
    context = {
        'current_user': get_current_user(user=request.user),
        'title': 'Список отчетов об инцидентах',
        'list_violation': ReportViolation.objects.all(),
    }
    return render(request, 'violation/list.html', context=context)


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
        list_violator.append([violator, SubnetOrg.objects.filter(subnet=violator.subnet)])
    context = {
        'current_user': get_current_user(user=request.user),
        'title': 'Отчет об инцидентах за ' + violation.date_violation.strftime('%d.%m.%Y'),
        'list_violator': list_violator,
    }
    return render(request, 'violation/show.html', context)


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
        'current_user': get_current_user(user=request.user),
        'title': 'Отчет об инцидентах узла ' + violator.ip_violator,
        'violator': violator,
        'list_incident': Incident.objects.filter(violator=violator),
    }

    return render(request, 'violation/incident.html', context)


######################################################################################################################
