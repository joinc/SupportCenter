from django.db import models
from Workplace.models import Subnet
from Organization.models import OrganizationSubnet

######################################################################################################################


class Report(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    date_report = models.DateField(
        verbose_name='Дата отчета',
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания отчета',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}'.format(self.date_report)

    class Meta:
        ordering = 'date_report',
        verbose_name = 'Отчет об инцидентах'
        verbose_name_plural = 'Отчеты об инцидентах'
        managed = True


######################################################################################################################


class FileReport(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    file = models.FileField(
        verbose_name='Файл с инцидентами',
        upload_to='violation/%Y/%m/%d/',
        null=True,
    )
    report = models.ForeignKey(
        Report,
        verbose_name='Отчет об инцидентах',
        null=True,
        blank=True,
        default=None,
        related_name='ReportFile',
        on_delete=models.CASCADE,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания файла',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0} - {1}'.format(self.report, self.file)

    class Meta:
        ordering = 'create_date',
        verbose_name = 'Файл с инцидентами'
        verbose_name_plural = 'Файлы с инцидентами'
        managed = True


######################################################################################################################


class Violator(models.Model):
    id = models.AutoField(
        primary_key=True,
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

    # def get_list_subnet(self):
    #     list_violator = []
    #     for violator in Violator.objects.filter(violation=self.violation):
    #         list_violator.append([violator, OrganizationSubnet.objects.filter(subnet=violator.subnet)])

    def __str__(self):
        return '{0}'.format(self.ip_violator)

    class Meta:
        ordering = 'ip_violator',
        verbose_name = 'Нарушитель'
        verbose_name_plural = 'Нарушители'
        managed = True


######################################################################################################################


class Incident(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    violator = models.ForeignKey(
        Violator,
        verbose_name='IP-адрес нарушителя',
        null=True,
        blank=True,
        default=None,
        related_name='IncidentViolator',
        on_delete=models.CASCADE,
    )
    violation = models.ForeignKey(
        Report,
        verbose_name='Отчет об инцидентах',
        null=True,
        blank=True,
        default=None,
        related_name='ReportIncident',
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
        return '{0}'.format(self.violator)

    class Meta:
        ordering = 'violator',
        verbose_name = 'Инциент'
        verbose_name_plural = 'Инциденты'
        managed = True


######################################################################################################################


class Violation(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    violator = models.ForeignKey(
        Violator,
        verbose_name='Нарушитель',
        null=True,
        blank=True,
        default=None,
        related_name='Violator',
        on_delete=models.CASCADE,
    )
    report = models.ForeignKey(
        Report,
        verbose_name='Отчет об инцидентах',
        null=True,
        blank=True,
        default=None,
        related_name='ReportViolation',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '{0} - {1}'.format(self.report, self.violator)

    class Meta:
        ordering = 'report', 'id',
        verbose_name = 'Нарушение'
        verbose_name_plural = 'Нарушения'
        managed = True


######################################################################################################################
