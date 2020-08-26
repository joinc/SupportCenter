# -*- coding: utf-8 -*-

from django import forms
from Main.models import Organization

######################################################################################################################


class FormOrganization(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['short_title', 'long_title', ]
        widgets = {
            'short_title': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Введите краткое название',
                }
            ),
            'long_title': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': 'Введите полное название',
                }
            ),
        }


######################################################################################################################


class FormOrganizationList(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['parent_organization', ]
        widgets = {
            'parent_organization': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


######################################################################################################################
