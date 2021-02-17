from django.db import models
from django.contrib.auth.models import User
from Organization.models import Organization, Department


######################################################################################################################

class CategoryPermission(models.Model):
    title = models.CharField(
        verbose_name='Название категории',
        max_length=64,
        default='',
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = 'title',
        verbose_name = 'Категория разрешения'
        verbose_name_plural = 'Категории разрешений'
        managed = True


######################################################################################################################


class Permission(models.Model):
    category = models.ForeignKey(
        CategoryPermission,
        verbose_name='Категория разрешения',
        null=True,
        blank=True,
        default=None,
        related_name='CategoryPermission',
        on_delete=models.SET_NULL,
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
        return '{0} - {1} ({2})'.format(self.category, self.title, self.name)

    class Meta:
        ordering = 'category', 'title',
        verbose_name = 'Разрешение'
        verbose_name_plural = 'Разрешения'
        managed = True


######################################################################################################################


class AccessRole(models.Model):
    title = models.CharField(
        verbose_name='Название роли',
        max_length=124,
        default='',
    )
    is_sample = models.BooleanField(
        verbose_name="Это шаблон роли",
        default=False,
    )
    user_list = models.BooleanField(
        verbose_name='Просматривать список пользователей',
        default=False,
    )
    user_edit = models.BooleanField(
        verbose_name='Добавлять, изменять, удалять пользователей',
        default=False,
    )
    signature_list = models.BooleanField(
        verbose_name='Просматривать список электронных подписей',
        default=False,
    )
    signature_edit = models.BooleanField(
        verbose_name='Добавлять, изменять, удалять электронные подписи',
        default=False,
    )
    signature_moderator = models.BooleanField(
        verbose_name='Модерировать электронные подписи',
        default=False,
    )
    organization_edit = models.BooleanField(
        verbose_name='Добавлять, изменять, удалять организации и отделы',
        default=False,
    )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        ordering = 'id',
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        managed = True


######################################################################################################################


class PresetAccess(models.Model):
    title = models.CharField(
        verbose_name='Название набора прав',
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
        verbose_name = 'Набор прав'
        verbose_name_plural = 'Наборы прав'
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
    access = models.ForeignKey(
        AccessRole,
        verbose_name='Роль доступа',
        null=True,
        blank=True,
        default=None,
        related_name='AccessRole',
        on_delete=models.SET_NULL,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания учетной записи',
        auto_now_add=True,
        null=True,
    )

    def block(self):
        self.blocked = True
        self.save(update_fields=['blocked', ])

    def unblock(self):
        self.blocked = False
        self.save(update_fields=['blocked', ])

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
        verbose_name='Набор прав',
        null=True,
        blank=True,
        default=None,
        related_name='PresetAccess',
        on_delete=models.CASCADE,
    )
    value = models.BooleanField(
        verbose_name='Значение',
        default=False,
    )

    def __str__(self):
        return '[{0}] {1} - {2}'.format(self.preset, self.permission, self.value)

    class Meta:
        ordering = 'permission',
        verbose_name = 'Право'
        verbose_name_plural = 'Права'
        managed = True


######################################################################################################################
