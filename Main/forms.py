# -*- coding: utf-8 -*-

from django import forms
from .models import Organization

######################################################################################################################


class FormUser(forms.Form):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите логин пользователя',
            }
        ),
        required=True,
    )
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите имя пользователя',
            }
        ),
        required=True,
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите фамилию пользователя',
            }
        ),
        required=True,
    )
    organization = forms.ChoiceField(
        label='Организация',
        widget=forms.Select(
            attrs={
                'class': 'custom-select',
            }
        ),
        choices=list(
            map(
                lambda x: [x['id'], x['short_title']],
                list(Organization.objects.values('id', 'short_title').all())
            )
        ),
        required=True,
    )
    access_user_list = forms.BooleanField(
        label='Просматривать список пользователей',
        required=False,
    )
    access_user_edit = forms.BooleanField(
        label='Добавлять, изменять, удалять пользователей',
        required=False,
    )


######################################################################################################################
