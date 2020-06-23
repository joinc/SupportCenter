from django.db import models
from django.contrib.auth.models import User

######################################################################################################################


class Organization(models.Model):
    short_title = models.CharField('Краткое название', max_length=124, default='', )
    long_title = models.CharField('Полное название', max_length=124, default='', )

    def __str__(self):
        return '{0}'.format(self.short_title)

    class Meta:
        ordering = 'short_title',
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        managed = True


######################################################################################################################


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    organization = models.ForeignKey(Organization, verbose_name='Организация', null=True, related_name='Organization',
                                     on_delete=models.SET_NULL, )
    create_date = models.DateTimeField('Дата создания учетной записи', auto_now_add=True, null=True, )
    blocked = models.BooleanField('Учетная запись заблокирована', default=False)

    def __str__(self):
        return '{0}'.format(self.user.get_full_name())

    class Meta:
        ordering = 'blocked', 'user',
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        managed = True

