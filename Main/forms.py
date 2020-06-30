# -*- coding: utf-8 -*-

from django import forms
from .models import Organization, AccessRole

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
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.TextInput(
            attrs={'type': 'password', 'class': 'form-control', 'autocomplete': 'off', }
        ),
        required=True,
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.TextInput(
            attrs={'type': 'password', 'class': 'form-control', 'autocomplete': 'off', }
        ),
        required=True,
    )
    change_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.TextInput(
            attrs={'type': 'password', 'class': 'form-control', 'autocomplete': 'off', }
        ),
        required=True,
    )
    change_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.TextInput(
            attrs={'type': 'password', 'class': 'form-control', 'autocomplete': 'off', }
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
    access_role = forms.ChoiceField(
        label='Роль',
        widget=forms.Select(
            attrs={
                'class': 'custom-select',
            }
        ),
        choices=list(
            map(
                lambda x: [x['id'], x['title']],
                list(AccessRole.objects.values('id', 'title').all())
            )
        ),
        required=True,
    )


######################################################################################################################
