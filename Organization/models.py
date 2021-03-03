from django.db import models
from Workplace.models import Address, Subnet

######################################################################################################################


class Organization(models.Model):
    short_title = models.CharField(
        verbose_name='Краткое название',
        max_length=124,
        default='',
    )
    long_title = models.CharField(
        verbose_name='Полное название',
        max_length=124,
        default='',
    )
    parent_organization = models.ForeignKey(
        'self',
        verbose_name='Вышестоящая организация',
        null=True,
        blank=True,
        default=None,
        related_name='ParentOrg',
        on_delete=models.SET_NULL,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания организации',
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


class Department(models.Model):
    title = models.CharField(
        verbose_name='Отдел',
        max_length=124,
        default='',
    )
    abbreviation = models.CharField(
        verbose_name='Аббревиатура',
        max_length=16,
        default='',
    )
    parent_department = models.ForeignKey(
        'self',
        verbose_name='Вышестоящий отдел',
        null=True,
        blank=True,
        default=None,
        related_name='ParentDep',
        on_delete=models.SET_NULL,
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        null=True,
        blank=True,
        default=None,
        related_name='OrganizationDep',
        on_delete=models.SET_NULL,
    )
    is_deleted = models.BooleanField(
        verbose_name='Удален',
        default=False,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания отдела',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = 'title',
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        managed = True


######################################################################################################################


class OrganizationAddress(models.Model):
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        null=True,
        related_name='OrganizationAddress',
        on_delete=models.SET_NULL,
    )
    address = models.ForeignKey(
        Address,
        verbose_name='Адрес организации',
        null=True,
        related_name='AddressOrganization',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return '{0} - {1}'.format(self.organization, self.address)

    class Meta:
        ordering = 'organization',
        verbose_name = 'Адрес орагизации'
        verbose_name_plural = 'Адреса организаций'
        managed = True


######################################################################################################################


class OrganizationSubnet(models.Model):
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        null=True,
        related_name='OrganizationSubnet',
        on_delete=models.SET_NULL,
    )
    subnet = models.ForeignKey(
        Subnet,
        verbose_name='Адрес организации',
        null=True,
        related_name='SubnetOrganization',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return '{0} - {1}'.format(self.subnet, self.organization)

    class Meta:
        ordering = 'subnet',
        verbose_name = 'Подсеть орагизации'
        verbose_name_plural = 'Подсети организаций'
        managed = True


######################################################################################################################
