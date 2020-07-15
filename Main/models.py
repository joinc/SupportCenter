from django.db import models
from django.contrib.auth.models import User

######################################################################################################################


class Organization(models.Model):
    short_title = models.CharField(
        'Краткое название',
        max_length=124,
        default='',
    )
    long_title = models.CharField(
        'Полное название',
        max_length=124,
        default='',
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания учетной записи',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}'.format(self.short_title)

    class Meta:
        ordering = 'short_title',
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        managed = True


######################################################################################################################
