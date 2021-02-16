from django.db import models
from Profile.models import UserProfile
from Signature.choices import STATUS_CHOICES
from Signature.certificate import Certificate as Cert

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
    file_name = models.CharField(
        verbose_name='Имя файла подписи',
        max_length=256,
        default='cert',
    )
    file_sign = models.FileField(
        verbose_name='Прикрепленный файл подписи',
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
    status = models.SmallIntegerField(
        verbose_name='Статус сертификата',
        choices=STATUS_CHOICES,
        default=0,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания учетной записи',
        auto_now_add=True,
        null=True,
    )

    def parse_file(self):
        certificate = Cert(self.file_sign.path)
        if not certificate.cert_format:
            return False
        else:
            iss, vlad_is = certificate.issuerCert()
            self.issuer = iss['CN']
            sub, vlad_sub = certificate.subjectCert()
            self.entity = sub['CN']
            self.serial = certificate.get_serial_number()
            valid = certificate.validityCert()
            self.valid_from = valid['not_before']
            self.valid_for = valid['not_after']
            return True

    def __str__(self):
        return '{0}'.format(self.entity)

    class Meta:
        ordering = 'status', 'valid_for',
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
        managed = True


######################################################################################################################
