# -*- coding: utf-8 -*-

from django import forms
from Violation.models import ReportViolation

######################################################################################################################


class FormViolation(forms.ModelForm):
    class Meta:
        model = ReportViolation
        fields = [
            'date_violation',
            'file_violation',
        ]
        widgets = {
            'date_violation': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'file_violation': forms.FileInput(
                attrs={
                    'class': 'form-control-file',
                }
            ),
        }
        labels = {
            'date_violation': 'Укажите дату формирования отчета об инцидентах',
            'file_violation': 'Выберите файлы отчета об инцидентах в формате csv',
        }


######################################################################################################################


# class FormViolation()