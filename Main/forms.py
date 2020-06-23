# -*- coding: utf-8 -*-

from django import forms
from .models import Organization

######################################################################################################################


class FormUser(forms.Form):
    organization_list = []
    for org in Organization.objects.all():
        organization_list.append([org.id, org.short_title])

    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Введите логин пользователя', }
        ),
        required=True,
    )
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Введите имя пользователя', }
        ),
        required=True,
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Введите фамилию пользователя', }
        ),
        required=True,
    )
    organization = forms.ChoiceField(
        label='Организация',
        widget=forms.Select(
            attrs={'class': 'custom-select'}
        ),
        choices=organization_list,
        required = True,
    )

######################################################################################################################
