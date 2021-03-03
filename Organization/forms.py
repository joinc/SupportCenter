# -*- coding: utf-8 -*-

from django import forms
from Organization.models import Organization, OrganizationAddress, OrganizationSubnet

######################################################################################################################


class FormOrganization(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            'short_title',
            'long_title',
            'parent_organization',
        ]
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
            'parent_organization': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


######################################################################################################################


class FormAddress(forms.ModelForm):
    class Meta:
        model = OrganizationAddress
        fields = [
            'address',
        ]
        widgets = {
            'address': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


######################################################################################################################


class FormSubnet(forms.ModelForm):
    class Meta:
        model = OrganizationSubnet
        fields = [
            'subnet',
        ]
        widgets = {
            'subnet': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


######################################################################################################################
