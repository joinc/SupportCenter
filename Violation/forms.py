# -*- coding: utf-8 -*-

from django import forms
from Violation.models import ReportViolation

######################################################################################################################


class FormViolation(forms.ModelForm):
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
        model = ReportViolation
        fields = [
            'date_violation',
        ]
        widgets = {
            'date_violation': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
        }
        labels = {
            'date_violation': 'Укажите дату формирования отчета об инцидентах',
        }


######################################################################################################################
