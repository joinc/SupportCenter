# -*- coding: utf-8 -*-

from Violation.models import Incident, Violator, FileReport, Violation
import csv

######################################################################################################################


def violation_create(report):
    """
    Загрузка отчета об инцидентах
    :param report:
    :return:
    """
    list_file_violation = FileReport.objects.filter(report=report)
    if list_file_violation:
        for file_violation in list_file_violation:
            with open(file_violation.file.path) as csv_file:
                reader = csv.reader(csv_file, delimiter=';')
                list_incident = []
                for index, row in enumerate(list(reader)):
                    if index > 0:
                        if not Incident.objects.filter(id_ids=row[0]).exists():
                            violator, create = Violator.objects.get_or_create(
                                ip_violator=row[5],
                            )
                            if create:
                                violator.set_subnet()
                            violation, create = Violation.objects.get_or_create(
                                violator=violator,
                                report=report,
                            )
                            incident = Incident(
                                violation=violation,
                                id_ids=row[0],
                                time_stamp=row[1],
                                code_incident=row[2],
                                source_ip=row[5],
                                source_port=row[6],
                                source_MAC=row[7],
                                destination_ip=row[8],
                                destination_port=row[9],
                                destination_MAC=row[10],
                                protocol_name=row[12],
                                class_incident=row[13],
                                message_incident=row[14],
                                priority=row[15],
                            )
                            list_incident.append(incident)
                Incident.objects.bulk_create(list_incident)
        return True
    return False


######################################################################################################################
