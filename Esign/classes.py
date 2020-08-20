# -*- coding: utf-8 -*-

from Esign.models import Certificate


######################################################################################################################


class EsignCount(object):

    def __init__(self, current_user):
        self.is_moderator = current_user.access.esign_moderator
        self.organization = current_user.organization

    def get_current_count(self):
        if self.is_moderator:
            return Certificate.objects.filter(is_current=True).count()
        else:
            return Certificate.objects.filter(is_current=True).filter(owner__organization=self.organization).count()

    def get_expires_count(self):
        if self.is_moderator:
            return Certificate.objects.filter(is_expires=True).count()
        else:
            return Certificate.objects.filter(is_expires=True).filter(owner__organization=self.organization).count()

    def get_expired_count(self):
        if self.is_moderator:
            return Certificate.objects.filter(is_expired=True).count()
        else:
            return Certificate.objects.filter(is_expired=True).filter(owner__organization=self.organization).count()

    def get_extended_count(self):
        if self.is_moderator:
            return Certificate.objects.filter(is_extended=True).count()
        else:
            return Certificate.objects.filter(is_extended=True).filter(owner__organization=self.organization).count()

    def get_terminate_count(self):
        if self.is_moderator:
            return Certificate.objects.filter(is_terminate=True).count()
        else:
            return Certificate.objects.filter(is_terminate=True).filter(owner__organization=self.organization).count()


######################################################################################################################
