# -*- coding: utf-8 -*-

from django import forms
from Profile.models import PresetAccess, Permission

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
        labels = {
            'title': 'Название шаблона разрешений',
        }


######################################################################################################################
