# -*- coding: utf-8 -*-

from django import forms
from Contract.models import Contract, Stage

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
                    'placeholder': 'Введите описание контракта',
                    'rows': '3',
                }
            ),
        }
        labels = {
            'title': 'Название контракта',
            'amount': 'Планируемая сумма контракта',
            'comment': 'Описание контракта',
        }


######################################################################################################################


class FormStage(forms.ModelForm):
    files = forms.FileField(
        label='Выберите файлы приложений',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control-file',
                'multiple': True
            }
        ),
        required=True,
    )

    class Meta:
        model = Stage
        fields = [
            'comment_stage',
        ]
        widgets = {
            'comment_stage': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Введите комметарий',
                }
            ),
        }
        labels = {
            'comment_stage': 'Комментарий стадии контракта',
        }


######################################################################################################################
