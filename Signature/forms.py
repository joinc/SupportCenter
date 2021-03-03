# -*- coding: utf-8 -*-

from django import forms
from Main.choices import SELECT_SIGNATURE_CHOICES
from Signature.models import Certificate

######################################################################################################################


class FormUpload(forms.ModelForm):
    status = forms.ChoiceField(
        label='Укажите статус данной электронной подписи',
        widget=forms.RadioSelect(),
        choices=SELECT_SIGNATURE_CHOICES,
    )

    class Meta:
        model = Certificate
        fields = [
            'file_sign',
        ]
        widgets = {
            'file_sign': forms.FileInput(
                attrs={
                    'class': 'form-control-file',
                }
            )
        }
        labels = {
            'file_sign': 'Укажите файл открытой части электронной подписи с расширением .cer',
        }


######################################################################################################################
