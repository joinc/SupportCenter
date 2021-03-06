# Generated by Django 3.1.4 on 2021-02-11 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Violation', '0006_auto_20210209_1540'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportviolation',
            options={'managed': True, 'ordering': ('date_violation',), 'verbose_name': 'Отчет об инцидентах', 'verbose_name_plural': 'Отчеты об инцидентах'},
        ),
        migrations.AlterModelOptions(
            name='violator',
            options={'managed': True, 'ordering': ('violation', 'ip_violator'), 'verbose_name': 'Нарушитель', 'verbose_name_plural': 'Нарушители'},
        ),
        migrations.AlterField(
            model_name='incident',
            name='violator',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='IncidentViolator', to='Violation.violator', verbose_name='IP-адрес нарушителя'),
        ),
        migrations.AlterField(
            model_name='reportviolation',
            name='file_violation',
            field=models.FileField(null=True, upload_to='violation/%Y/%m/%d/bfb9aeef08e944529b11308532ccb2ed', verbose_name='Файл с инцидентами'),
        ),
    ]
