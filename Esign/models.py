from django.db import models
from Profile.models import UserProfile
import fsb795

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
        upload_to='sign/%Y/%m/%d',
        null=True,
    )
    renew = models.ForeignKey(
        'self',
        verbose_name='Продляет сертификат',
        null=True,
        default=None,
        related_name='EsignRenew',
        on_delete=models.SET_NULL,
    )
    extended = models.ForeignKey(
        'self',
        verbose_name='Продлен сертификатом',
        null=True,
        default=None,
        related_name='EsignExtended',
        on_delete=models.SET_NULL,
    )
    is_current = models.BooleanField(
        verbose_name='Действует',
        default=True,
    )
    is_expires = models.BooleanField(
        verbose_name='Истекает',
        default=False,
    )
    is_expired = models.BooleanField(
        verbose_name='Истек',
        default=False,
    )
    is_extended = models.BooleanField(
        verbose_name='Продлен',
        default=False,
    )
    is_terminate = models.BooleanField(
        verbose_name='Аннулирован',
        default=False,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания учетной записи',
        auto_now_add=True,
        null=True,
    )

    def parse_file(self):
        certificate = fsb795.Certificate(self.file_sign.path)
        if certificate.pyver == '':
            return False
        else:
            iss, vlad_is = certificate.issuerCert()
            self.issuer = iss['CN']
            sub, vlad_sub = certificate.subjectCert()
            self.entity = sub['CN']
            serial = str(hex(certificate.serialNumber()))
            # Убираем из серийного номера символ (x) - обозначение шестнадцатеричной строки
            serial = serial[0] + serial[2:]
            self.serial = serial
            valid = certificate.validityCert()
            self.valid_from = valid['not_before']
            self.valid_for = valid['not_after']
            return True

    def __str__(self):
        return '{0}'.format(self.entity)

    class Meta:
        ordering = 'is_terminate', 'is_extended', 'valid_for',
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
        managed = True


######################################################################################################################
