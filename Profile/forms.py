# -*- coding: utf-8 -*-

from django import forms
from Profile.models import AccessRole, UserProfile

######################################################################################################################


class FormPassword(forms.Form):
    password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.TextInput(
            attrs={
                'type': 'password',
                'class': 'form-control',
                'autocomplete': 'off',
            }
        ),
        required=True,
    )
    password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.TextInput(
            attrs={
                'type': 'password',
                'class': 'form-control',
                'autocomplete': 'off',
            }
        ),
        required=True,
    )


######################################################################################################################


class FormAccessList(forms.ModelForm):
    class Meta:
        model = AccessRole
        fields = [
            'user_list',
            'user_edit',
            'esign_list',
            'esign_edit',
            'esign_moderator',
            'organization_edit',
        ]
        widgets = {
            'user_list': forms.CheckboxInput(
                attrs={
                    'class': 'custom-control-input',
                }
            ),
            'user_edit': forms.CheckboxInput(
                attrs={
                    'class': 'custom-control-input',
                }
            ),
            'esign_list': forms.CheckboxInput(
                attrs={
                    'class': 'custom-control-input',
                }
            ),
            'esign_edit': forms.CheckboxInput(
                attrs={
                    'class': 'custom-control-input',
                }
            ),
            'esign_moderator': forms.CheckboxInput(
                attrs={
                    'class': 'custom-control-input',
                }
            ),
            'organization_edit': forms.CheckboxInput(
                attrs={
                    'class': 'custom-control-input',
                }
            ),
        }


######################################################################################################################


class FormUserSearch(forms.Form):
    find = forms.CharField(
        label='Поиск пользователя',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Введите логин или фамилию пользователя',
            }
        ),
        required=False,
    )


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
        required=False,
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
        required=False,
    )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                'placeholder': 'Введите электронный адрес',
            }
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
                list(AccessRole.objects.values('id', 'title').filter(is_sample=True))
            )
        ),
        required=True,
    )


######################################################################################################################
