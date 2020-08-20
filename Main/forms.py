# -*- coding: utf-8 -*-

from django import forms
from Main.models import Organization

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
    parent_organization = forms.ChoiceField(
        label='Вышестоящая организация',
        widget=forms.Select(
            attrs={
                'class': 'custom-select',
            }
        ),
        choices=[[0, '----- Выберите вышестоящую организацию -----']] + list(
            map(
                lambda x: [x['id'], x['short_title']],
                list(Organization.objects.values('id', 'short_title').all())
            )
        ),
        required=False,
    )


######################################################################################################################
