from django.db import models

######################################################################################################################


class Address(models.Model):
    index = models.CharField(
        verbose_name='Индекс',
        max_length=24,
        default='',
    )
    locality = models.CharField(
        verbose_name='Населенный пункт',
        max_length=256,
        default='',
    )
    street = models.CharField(
        verbose_name='Название улицы',
        max_length=124,
        default='',
    )
    house = models.CharField(
        verbose_name='Номер дома',
        max_length=8,
        default='',
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания адреса расположения',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}, {1}, {2}, {3}'.format(self.index, self.locality, self.street, self.house)

    class Meta:
        ordering = 'street', 'house',
        verbose_name = 'Адрес расположения'
        verbose_name_plural = 'Адреса расположения'
        managed = True


######################################################################################################################


class TypeEquipment(models.Model):
    title = models.CharField(
        verbose_name='Тип оборудования',
        max_length=124,
        default='',
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания типа оборудования',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = 'title',
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'
        managed = True


######################################################################################################################


class Placement(models.Model):
    address = models.ForeignKey(
        Address,
        verbose_name='Адрес расположения',
        null=True,
        blank=True,
        default=None,
        related_name='AddressPlacement',
        on_delete=models.SET_NULL,
    )
    cabinet = models.CharField(
        verbose_name='Кабинет',
        max_length=8,
        default='',
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания расположения',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}, каб. {1}'.format(self.address, self.cabinet)

    class Meta:
        ordering = 'address', 'cabinet',
        verbose_name = 'Располежение'
        verbose_name_plural = 'Расположения'
        managed = True


######################################################################################################################


class Workplace(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=124,
        default='',
    )
    placement = models.ForeignKey(
        Placement,
        verbose_name='Расположение',
        null=True,
        blank=True,
        default=None,
        related_name='Placement',
        on_delete=models.SET_NULL,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания организации',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = 'title',
        verbose_name = 'Рабочее место'
        verbose_name_plural = 'Рабочие места'
        managed = True


######################################################################################################################


class Equipment(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=124,
        default='',
    )
    inventory_number = models.CharField(
        verbose_name='Инвентарный номер',
        max_length=124,
        default='',
    )
    type = models.ForeignKey(
        TypeEquipment,
        verbose_name='Тип оборудования',
        null=True,
        blank=True,
        default=None,
        related_name='TypeEquipment',
        on_delete=models.SET_NULL,
    )
    workplace = models.ForeignKey(
        Workplace,
        verbose_name='Рабочее место',
        null=True,
        blank=True,
        default=None,
        related_name='Workplace',
        on_delete=models.SET_NULL,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания оборудования',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = 'title',
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудования'
        managed = True


######################################################################################################################


class Subnet(models.Model):
    subnet = models.CharField(
        verbose_name='Подсеть',
        max_length=24,
        default='',
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания подсети',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}'.format(self.subnet)

    class Meta:
        ordering = 'subnet',
        verbose_name = 'Подсеть'
        verbose_name_plural = 'Подсети'
        managed = True


######################################################################################################################
