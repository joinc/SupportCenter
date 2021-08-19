# -*- coding: utf-8 -*-

from django import forms
from Violation.models import Report

######################################################################################################################


class FormReport(forms.ModelForm):
    files = forms.FileField(
        label='Выберите файлы отчета об инцидентах в формате csv',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control-file',
                'multiple': True
            }
        ),
        required=True,
    )

    class Meta:
        model = Report
        fields = [
            'date_report',
        ]
        widgets = {
            'date_report': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
        }
        labels = {
            'date_report': 'Укажите дату формирования отчета об инцидентах',
        }


######################################################################################################################
