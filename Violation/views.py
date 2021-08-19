# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from Violation.models import Incident, Violator, Report, FileReport
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
                file_violation = FileReport(violation=report, )
                file_violation.file.save(file.name, file)
                file_violation.save()
            if violation_create(report_violation=report_violation):
                messages.success(request, 'Отчет {0} успешно загружен.'.format(report_violation))
                return redirect(reverse('violation_show', args=(report_violation.id, )))
            else:
                messages.error(request, 'Ошибка при загрузке файлов отчета')
        else:
            messages.error(request, 'Ошибка при загрузке отчета. Форма заполнена не корректно.')
    context = {
        'current_user': get_profile(user=request.user),
        'title': 'Загрузка инцидентов',
        'list_breadcrumb': (
            (reverse('violation_list'), 'Список отчетов об инцидентах'),
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
    is_moderator = current_user.access(list_permission=['violation_moderator', ])
    # if is_moderator:
    #     list_violator = Violator.objects.filter(
    #         violation=violation,
    #     )
    # else:
    #     list_violator = Violator.objects.filter(
    #         violation=violation,
    #         subnet__SubnetOrganization__organization=current_user.organization,
    #     )
    list_violator = Violator.objects.all()
    list_violation = []
    for violator in list_violator:
        list_violation.append([violator, OrganizationSubnet.objects.filter(subnet=violator.subnet), ])
    context = {
        'current_user': current_user,
        'title': 'Отчет об инцидентах за ' + report.date_report.strftime('%d.%m.%Y'),
        'list_breadcrumb': (
            (reverse('violation_list'), 'Список отчетов об инцидентах'),
        ),
        'report': report,
        'list_violation': list_violation,
        'violation_moderator': current_user.access(list_permission=['violation_moderator', ]),
        'violation_edit': current_user.access(list_permission=['violation_edit', ]),
    }
    return render(request=request, template_name='violation/report_show.html', context=context)


######################################################################################################################


@permission_required(['violation_list', 'violation_edit', 'violation_moderator', ])
def violator_show(request, report_id, violator_id):
    """
    Список нарушителей в отчете об инцидентах
    :param request:
    :param report_id:
    :param violator_id:
    :return:
    """
    current_user = get_profile(user=request.user)
    is_moderator = current_user.access(list_permission=['violation_moderator', ])
    is_editor = current_user.access(list_permission=['violation_edit', ])
    violator = get_object_or_404(Violator, id=violator_id)
    violation = get_object_or_404(Report, id=report_id)
    if OrganizationSubnet.objects.filter(subnet=violator.subnet, organization=current_user.organization).exists() or is_moderator:
        if request.POST:
            ...
        else:
            ...

    else:
        return redirect(reverse('violation_list'))
    print(violation.id)
    context = {
        'current_user': current_user,
        'title': 'Отчет об инцидентах узла ' + violator.ip_violator,
        'list_breadcrumb': (
            (reverse('violation_list'), 'Список отчетов об инцидентах'),
            (reverse('violation_show', args=(violation.id, )), 'Отчет об инцидентах за {0}'.format(violation.date_report.strftime('%d.%m.%Y'))),
        ),
        'violator': violator,
        'list_incident': Incident.objects.filter(violator=violator),
    }

    return render(request=request, template_name='violation/incident.html', context=context)


######################################################################################################################
