# -*- coding: utf-8 -*-

from django import forms
from Signature.choices import SELECT_CHOICES

######################################################################################################################

# class FormUpload1(forms.ModelForm):


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
    select = forms.ChoiceField(
        label='Выберите статус',
        widget=forms.RadioSelect(),
        choices=SELECT_CHOICES,
    )


######################################################################################################################
