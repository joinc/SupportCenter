# -*- coding: utf-8 -*-

from django import forms
from Profile.models import AccessRole, UserProfile
from django.contrib.auth.models import User


######################################################################################################################


class FormSearchUser(forms.Form):
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


class FormCreateUser(forms.ModelForm):
    password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.TextInput(
            attrs={
                'type': 'password',
                'class': 'form-control',
                'autocomplete': 'off',
            }
        ),
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.',
        required=True,
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
        ]
        labels = {
            'username': 'Логин пользователя',
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите имя пользователя',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите фамилию пользователя',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите логин пользователя',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'type': 'email',
                    'class': 'form-control',
                    'placeholder': 'Введите электронный адрес',
                }
            ),
            'password': forms.TextInput(
                attrs={
                    'type': 'password',
                    'class': 'form-control',
                    'autocomplete': 'off',
                }
            ),
        }
        help_texts = {
            'username': 'Обязательное поле. Только английские буквы.',
            'password': 'Пароль не должен совпадать с логином и состоять только из цифр. '
                        'Пароль должен содержать как минимум 8 символов.',
        }


######################################################################################################################


class FormChangePassword(forms.Form):
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


class FormEditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите имя пользователя',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите фамилию пользователя',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'type': 'email',
                    'class': 'form-control',
                    'placeholder': 'Введите электронный адрес',
                }
            ),
        }


######################################################################################################################


class FormAccessRole(forms.Form):
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


class FormAccessList(forms.ModelForm):
    class Meta:
        model = AccessRole
        # exclude = ['title']
        fields = [
            'user_list',
            'user_edit',
            'esign_list',
            'esign_edit',
            'esign_moderator',
            'organization_edit',
        ]
        widgets = {}
        for field in fields:
            widgets.update(
                {
                    field: forms.CheckboxInput(
                        attrs={
                            'class': 'custom-control-input',
                        }
                    )
                }
            )


######################################################################################################################


class FormOrganization(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'organization',
        ]
        widgets = {
            'organization': forms.Select(
                attrs={
                    'class': 'custom-select',
                }
            ),
        }
        labels = {
            'organization': 'Организация',
        }


######################################################################################################################
