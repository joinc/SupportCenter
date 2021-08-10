from django.db import models

######################################################################################################################


class Status(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        verbose_name='Название стадии',
        max_length=64,
        default='',
    )
    order = models.SmallIntegerField(
        verbose_name='Порядок в списке стадий',
        default=0,
    )
    next_status = models.ForeignKey(
        'self',
        verbose_name='Следующая стадия',
        related_name='NextStatus',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = 'order', 'title',
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        managed = True


######################################################################################################################


class Contract(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        verbose_name='Наименование',
        max_length=124,
        default='',
    )
    amount = models.CharField(
        verbose_name='Плановая сумма',
        max_length=124,
        default='',
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        default='',
    )
    closed = models.BooleanField(
        verbose_name='Закрыт',
        default=False,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания контракта',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = 'title',
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'
        managed = True


######################################################################################################################


class Stage(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    contract = models.ForeignKey(
        Contract,
        verbose_name='Контракт',
        null=True,
        related_name='ContractStatus',
        on_delete=models.SET_NULL,
    )
    status = models.ForeignKey(
        Status,
        verbose_name='Статус контракта',
        null=True,
        related_name='StatusContract',
        on_delete=models.SET_NULL,
    )
    comment_stage = models.TextField(
        verbose_name='Комментарий',
        default='',
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания стадии',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0} - {1}'.format(self.contract, self.status)

    class Meta:
        ordering = 'status', 'contract',
        verbose_name = 'Стадия'
        verbose_name_plural = 'Стадии'
        managed = True


######################################################################################################################


class Attache(models.Model):
    name = models.CharField(
        verbose_name='Название файла',
        max_length=124,
        default='',
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to='contract/attache/%Y/%m/%d',
        null=True,
        blank=True,
    )
    stage = models.ForeignKey(
        Stage,
        verbose_name='Стадия',
        null=True,
        related_name='AttacheStage',
        on_delete=models.SET_NULL,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания файла',
        auto_now_add=True,
        null=True,
    )

    def get_human_size(self):
        value = self.file.size
        if value < 512000:
            value = value / 1024.0
            ext = 'Кб'
        elif value < 4194304000:
            value = value / 1048576.0
            ext = 'Мб'
        else:
            value = value / 1073741824.0
            ext = 'Гб'
        return '{0} {1}'.format(str(round(value, 2)), ext)

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering = 'create_date',
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'
        managed = True


######################################################################################################################
