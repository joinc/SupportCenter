# -*- coding: utf-8 -*-

from django import forms

######################################################################################################################


class FormUpload(forms.Form):
    file = forms.FileField(
        label='Укажите файл открытой части электронной подписи с расширением .cer',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control-file',

            }
        ),
        required=True,
    )


######################################################################################################################
