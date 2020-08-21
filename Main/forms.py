# -*- coding: utf-8 -*-

from django import forms

######################################################################################################################


class FormOrganization(forms.Form):
    short_title = forms.CharField(
        label='Краткое название',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите краткое название',
            }
        ),
        required=True,
    )
    long_title = forms.CharField(
        label='Полное название',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите полное название',
            }
        ),
        required=True,
    )


######################################################################################################################
