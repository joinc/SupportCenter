# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from Violation.models import Incident, Report, FileReport, Violation
from Violation.forms import FormReport
from Violation.tools import violation_create
from Organization.models import OrganizationSubnet
from Main.decorators import permission_required
from Main.tools import get_profile

######################################################################################################################


@permission_required(['violation_list', 'violation_edit', 'violation_moderator', ])
def report_list(request):
    """
    Отображает список отчетов об инцидентах
    :param request:
    :return: HttpResponse
    """
    current_user = get_profile(user=request.user)
    context = {
        'current_user': current_user,
        'title': 'Список отчетов об инцидентах',
        'list_report': Report.objects.all(),
        'violation_moderator': current_user.access(list_permission=['violation_moderator', ]),
    }
    return render(request=request, template_name='violation/report_list.html', context=context)


######################################################################################################################


@permission_required(['violation_moderator', ])
def report_load(request):
    """
    Загрузка отчета о нарушениях
    :param request:
    :return:
    """
    if request.POST:
        report = Report()
        formset = FormReport(request.POST, request.FILES, instance=report)
        if formset.is_valid():
            formset.save()
            for file in request.FILES.getlist('files'):
                file_violation = FileReport(report=report, )
                file_violation.file.save(file.name, file)
                file_violation.save()
            if violation_create(report=report):
                messages.success(request, 'Отчет {0} успешно загружен.'.format(report))
                return redirect(reverse('violation:report_show', args=(report.id, )))
            else:
                messages.error(request, 'Ошибка при загрузке файлов отчета')
        else:
            messages.error(request, 'Ошибка при загрузке отчета. Форма заполнена не корректно.')
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Загрузка инцидентов',
        'list_breadcrumb': (
            (reverse('violation:report_list'), 'Список отчетов об инцидентах'),
        ),
        'form_violation': FormReport(),
    }
    return render(request=request, template_name='violation/report_load.html', context=context)


######################################################################################################################


@permission_required(['violation_list', 'violation_edit', 'violation_moderator', ])
def report_show(request, report_id):
    """
    Список нарушителей в отчете об инцидентах
    :param request:
    :param report_id:
    :return:
    """
    current_user = get_profile(user=request.user)
    report = get_object_or_404(Report, id=report_id)
    # is_moderator = current_user.access(list_permission=['violation_moderator', ])
    # if is_moderator:
    #     list_violator = Violator.objects.filter(
    #         violation=violation,
    #     )
    # else:
    #     list_violator = Violator.objects.filter(
    #         violation=violation,
    #         subnet__SubnetOrganization__organization=current_user.organization,
    #     )

    list_violation = Violation.objects.filter(report=report)
    list_violation_org = []
    for violation in list_violation:
        list_violation_org.append(
            [
                violation,
                OrganizationSubnet.objects.filter(subnet=violation.violator.subnet),
                Incident.objects.filter(violation=violation, priority='high').count(),
                Incident.objects.filter(violation=violation, priority='mid').count(),
            ]
        )
    context = {
        'current_user': current_user,
        'title': 'Отчет об инцидентах за ' + report.date_report.strftime('%d.%m.%Y'),
        'list_breadcrumb': (
            (reverse('violation:report_list'), 'Список отчетов об инцидентах'),
        ),
        'report': report,
        'list_violation_org': list_violation_org,
        'count_violation': list_violation.count(),
        'violation_moderator': current_user.access(list_permission=['violation_moderator', ]),
        'violation_edit': current_user.access(list_permission=['violation_edit', ]),
    }
    return render(request=request, template_name='violation/report_show.html', context=context)


######################################################################################################################


@permission_required(['violation_list', 'violation_edit', 'violation_moderator', ])
def violation_show(request, violation_id):
    """
    Список нарушителей в отчете об инцидентах
    :param request:
    :param violation_id:
    :return:
    """
    current_user = get_profile(user=request.user)
    # is_moderator = current_user.access(list_permission=['violation_moderator', ])
    # is_editor = current_user.access(list_permission=['violation_edit', ])
    violation = get_object_or_404(Violation, id=violation_id)

    # if OrganizationSubnet.objects.filter(subnet=violator.subnet, organization=current_user.organization).exists()
    # or is_moderator:
    #     if request.POST:
    #         ...
    #     else:
    #         ...
    # else:
    #     return redirect(reverse('report_list'))
    context = {
        'current_user': current_user,
        'title': 'Отчет об инцидентах узла ' + violation.violator.ip_violator,
        'list_breadcrumb': (
            (
                reverse('violation:report_list'),
                'Список отчетов об инцидентах',
            ),
            (
                reverse('violation:report_show', args=(violation.report.id, )),
                'Отчет об инцидентах за {0}'.format(violation.report.date_report.strftime('%d.%m.%Y')),
            ),
        ),
        'violation': violation,
        'list_incident': Incident.objects.filter(violation=violation),
    }

    return render(request=request, template_name='violation/incident.html', context=context)


######################################################################################################################
