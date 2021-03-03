# -*- coding: utf-8 -*-

from django import forms
from Profile.models import PresetAccess
from Workplace.models import Address, Subnet

######################################################################################################################


class FormPresetTitle(forms.ModelForm):
    class Meta:
        model = PresetAccess
        fields = [
            'title',
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Введите название шаблона разрешений',
                }
            ),
        }


######################################################################################################################


class FormAddress(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'index',
            'locality',
            'street',
            'house',
        ]
        widgets = {
            'index': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Введите индекс',
                }
            ),
            'locality': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Введите название населенного пункта',
                }
            ),
            'street': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Введите название улицы',
                }
            ),
            'house': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Введите номер дома',
                }
            ),
        }


######################################################################################################################


class FormSubnet(forms.ModelForm):
    class Meta:
        model = Subnet
        fields = [
            'subnet',
        ]
        widgets = {
            'subnet': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Введите подсеть, пример: 192.168.1.0/24',
                }
            ),
        }


######################################################################################################################
