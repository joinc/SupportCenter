# -*- coding: utf-8 -*-

from django import forms
from Esign.choices import STATUS_CHOICES

######################################################################################################################


class FormUpload(forms.Form):
    file = forms.FileField(
        label='Укажите файл открытой части электронной подписи с расширением .cer',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file',
            }
        ),
        required=True,
    )
    status = forms.ChoiceField(
        label='Выберите статус',
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES
    )


######################################################################################################################
