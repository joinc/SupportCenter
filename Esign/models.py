from django.db import models
from Profile.models import UserProfile

######################################################################################################################


class Certificate(models.Model):
    issuer = models.CharField(
        verbose_name='Издатель',
        max_length=124,
        default='',
    )
    entity = models.CharField(
        verbose_name='Субъект',
        max_length=124,
        default='',
    )
    serial = models.CharField(
        verbose_name='Серийной номер',
        max_length=64,
        default='',
    )
    valid_from = models.DateTimeField(
        verbose_name='Действителен с',
        null=True,
    )
    valid_for = models.DateTimeField(
        verbose_name='Действителен по',
        null=True,
    )
    owner = models.ForeignKey(
        UserProfile,
        verbose_name='Модератор подписи',
        null=True,
        related_name='UserProfile',
        on_delete=models.SET_NULL,
    )
    file_sign = models.FileField(
        verbose_name='Прикрепленный файл',
        upload_to='upload/sign/%Y/%m/%d',
        null=True,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания учетной записи',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}'.format(self.entity)

    class Meta:
        ordering = '-valid_for',
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
        managed = True

