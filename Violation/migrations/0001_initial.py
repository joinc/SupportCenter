# Generated by Django 3.1.4 on 2021-02-04 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DateViolation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата отчета')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания отчета')),
            ],
            options={
                'verbose_name': 'Дата отчета',
                'verbose_name_plural': 'Даты отчетов',
                'ordering': ('date',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='IPViolator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_violator', models.CharField(default='', max_length=24, verbose_name='IP-адрес нарушителя')),
                ('date_violation', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='DateViolation', to='Violation.dateviolation', verbose_name='Дата отчета')),
            ],
            options={
                'verbose_name': 'IP-адрес нарушителя',
                'verbose_name_plural': 'IP-адреса нарушителей',
                'ordering': ('date_violation', 'ip_violator'),
                'managed': True,
            },
        ),
    ]
