# -*- coding: utf-8 -*-

from ipaddress import IPv4Address, IPv4Network
from Violation.models import Incident, Violator, FileReport
from Workplace.models import Subnet
import csv

######################################################################################################################


def violation_create(report_violation):
    """
    Загрузка отчета об инцидентах
    :param report_violation:
    :return:
    """
    list_file_violation = FileReport.objects.filter(violation=report_violation)
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
                                for subnet in Subnet.objects.all():
                                    if IPv4Address(violator.ip_violator) in IPv4Network(subnet.subnet):
                                        violator.subnet = subnet
                                        violator.save(update_fields=['subnet'])
                            incident = Incident(
                                violator=violator,
                                violation=report_violation,
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
