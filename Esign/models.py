from django.db import models

######################################################################################################################


class Certificate(models.Model):
    title = models.CharField(
        'Название',
        max_length=124,
        default='',
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания учетной записи',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = 'title',
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
        managed = True

