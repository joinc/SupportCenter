from django.db import models
from uuid import uuid4
from Workplace.models import Subnet
from Organization.models import SubnetOrg

######################################################################################################################


class ReportViolation(models.Model):
    date_violation = models.DateField(
        verbose_name='Дата отчета',
    )
    file_violation = models.FileField(
        verbose_name='Файл с инцидентами',
        upload_to='violation/%Y/%m/%d/'+uuid4().hex,
        null=True,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания отчета',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}'.format(self.date_violation)

    class Meta:
        ordering = 'date_violation',
        verbose_name = 'Отчет об инцидентах'
        verbose_name_plural = 'Отчеты об инцидентах'
        managed = True


######################################################################################################################


class Violator(models.Model):
    violation = models.ForeignKey(
        ReportViolation,
        verbose_name='Дата отчета',
        null=True,
        blank=True,
        default=None,
        related_name='DateViolation',
        on_delete=models.CASCADE,
    )
    ip_violator = models.CharField(
        verbose_name='IP-адрес нарушителя',
        max_length=24,
        default='',
    )
    subnet = models.ForeignKey(
        Subnet,
        null=True,
        blank=True,
        default=None,
        related_name='Subnet',
        on_delete=models.SET_NULL,
    )

    def get_list_subnet(self):
        list_violator = []
        for violator in Violator.objects.filter(violation=self):
            list_violator.append([violator, SubnetOrg.objects.filter(subnet=violator.subnet)])

    def __str__(self):
        return '{0} - {1}'.format(self.ip_violator, self.violation)

    class Meta:
        ordering = 'violation', 'ip_violator',
        verbose_name = 'Нарушитель'
        verbose_name_plural = 'Нарушители'
        managed = True


######################################################################################################################


class Incident(models.Model):
    violator = models.ForeignKey(
        Violator,
        verbose_name='IP-адрес нарушителя',
        null=True,
        blank=True,
        default=None,
        related_name='IncidentViolator',
        on_delete=models.CASCADE,
    )
    id_ids = models.CharField(
        verbose_name='id_ids',
        max_length=24,
        default='',
    )
    time_stamp = models.CharField(
        verbose_name='Timestamp',
        max_length=64,
        default='',
    )
    code_incident = models.CharField(
        verbose_name='Code',
        max_length=64,
        default='',
    )
    aggregated = models.CharField(
        verbose_name='Aggregated',
        max_length=8,
        default='',
    )
    aggregation_period = models.CharField(
        verbose_name='Aggregation period',
        max_length=8,
        default='',
    )
    source_ip = models.CharField(
        verbose_name='Src IP',
        max_length=24,
        default='',
    )
    source_port = models.CharField(
        verbose_name='Src port',
        max_length=8,
        default='',
    )
    source_MAC = models.CharField(
        verbose_name='Src MAC',
        max_length=24,
        default='',
    )
    destination_ip = models.CharField(
        verbose_name='Dst IP',
        max_length=24,
        default='',
    )
    destination_port = models.CharField(
        verbose_name='Dst port',
        max_length=8,
        default='',
    )
    destination_MAC = models.CharField(
        verbose_name='Dst MAC',
        max_length=24,
        default='',
    )
    protocol = models.CharField(
        verbose_name='Protocol',
        max_length=8,
        default='',
    )
    protocol_name = models.CharField(
        verbose_name='Protocol name',
        max_length=8,
        default='',
    )
    class_incident = models.CharField(
        verbose_name='Class',
        max_length=24,
        default='',
    )
    message_incident = models.CharField(
        verbose_name='Msg',
        max_length=124,
        default='',
    )
    priority = models.CharField(
        verbose_name='Priority',
        max_length=24,
        default='',
    )

    def __str__(self):
        return '{0} - {1}'.format(self.id_ids, self.time_stamp)

    class Meta:
        ordering = 'id_ids', 'time_stamp',
        verbose_name = 'Инциент'
        verbose_name_plural = 'Инциденты'
        managed = True


######################################################################################################################
