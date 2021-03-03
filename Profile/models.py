from django.db import models
from django.contrib.auth.models import User
from Organization.models import Organization, Department
from Main.choices import FULL_MENU, CATEGORY_PERMISSION


######################################################################################################################


class PresetAccess(models.Model):
    title = models.CharField(
        verbose_name='Название шаблона разрешений',
        max_length=64,
        default='',
    )
    is_sample = models.BooleanField(
        verbose_name="Является шаблонным набором прав",
        default=False,
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = 'title',
        verbose_name = 'Шаблон разрешений'
        verbose_name_plural = 'Шаблоны разрешений'
        managed = True


######################################################################################################################


class Permission(models.Model):
    category = models.SmallIntegerField(
        verbose_name='Категория разрешения',
        choices=CATEGORY_PERMISSION,
        default=0,
        null=False,
        blank=False,
    )
    title = models.CharField(
        verbose_name='Название разрешения',
        max_length=64,
        default='',
    )
    name = models.CharField(
        verbose_name='Обозначение разрешения',
        max_length=64,
        default='',
    )

    def __str__(self):
        return '{0} - {1} ({2})'.format(self.get_category_display(), self.title, self.name)

    class Meta:
        ordering = 'category', 'title',
        verbose_name = 'Разрешение'
        verbose_name_plural = 'Разрешения'
        managed = True


######################################################################################################################


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        null=True,
        blank=True,
        default=None,
        related_name='Organization',
        on_delete=models.SET_NULL,
    )
    department = models.ForeignKey(
        Department,
        verbose_name='Отдел',
        null=True,
        blank=True,
        default=None,
        related_name='Department',
        on_delete=models.SET_NULL,
    )
    blocked = models.BooleanField(
        verbose_name='Учетная запись заблокирована',
        default=False,
    )
    preset = models.ForeignKey(
        PresetAccess,
        verbose_name='Набор прав',
        null=True,
        blank=True,
        default=None,
        related_name='PresetAccess_UserProfile',
        on_delete=models.CASCADE,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания учетной записи',
        auto_now_add=True,
        null=True,
    )

    def block(self):
        """
        Блокирует пользователя
        :return:
        """
        self.blocked = True
        self.save(update_fields=['blocked', ])

    def unblock(self):
        """
        Разблокирует пользователя
        :return:
        """
        self.blocked = False
        self.save(update_fields=['blocked', ])

    def access(self, list_permission):
        """
        Возвращает значение, есть или нет у пользователя права из списка
        :param list_permission:
        :return:
        """
        for permission in list_permission:
            if Access.objects.filter(
                    permission__name=permission,
                    preset__PresetAccess_UserProfile=self,
                    value=True,
            ).exists():
                return True
        return False

    def get_menu(self):
        """
        Формирует доступные элементы меню в зависимости от прав
        :return:
        """
        menu = []
        for item in FULL_MENU:
            if self.access(list_permission=item[0]):
                menu.append(item)
        return menu

    def __str__(self):
        return '{0}'.format(self.user.get_full_name())

    class Meta:
        ordering = 'blocked', 'user',
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        managed = True


######################################################################################################################


class Access(models.Model):
    permission = models.ForeignKey(
        Permission,
        verbose_name='Разрешение',
        null=True,
        blank=True,
        default=None,
        related_name='AccessPermission',
        on_delete=models.CASCADE,
    )
    preset = models.ForeignKey(
        PresetAccess,
        verbose_name='Шаблон разрешений',
        null=True,
        blank=True,
        default=None,
        related_name='PresetAccess_Access',
        on_delete=models.CASCADE,
    )
    value = models.BooleanField(
        verbose_name='Значение',
        default=False,
    )

    def __str__(self):
        return '[{0}] {1} - {2}'.format(self.preset, self.permission, self.value)

    class Meta:
        ordering = 'preset', 'permission',
        verbose_name = 'Право'
        verbose_name_plural = 'Права'
        managed = True


######################################################################################################################
