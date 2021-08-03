# -*- coding: utf-8 -*-

from django import forms
from Contract.models import Contract

######################################################################################################################


class FormContract(forms.ModelForm):
    name = 'Добавление контракта'

    class Meta:
        model = Contract
        fields = [
            'title',
            'amount',
            'comment',
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Введите название контракта',
                }
            ),
            'amount': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Введите сумму контракта',
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Введите комметтарий',
                }
            ),
        }


######################################################################################################################
