from django.db import models
from django.contrib.auth.models import User
from Organization.models import Organization, Department

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
    esign_list = models.BooleanField(
        verbose_name='Просматривать список электронных подписей',
        default=False,
    )
    esign_edit = models.BooleanField(
        verbose_name='Добавлять, изменять, удалять электронные подписи',
        default=False,
    )
    esign_moderator = models.BooleanField(
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
        self.save()

    def unblock(self):
        self.blocked = False
        self.save()

    def __str__(self):
        return '{0}'.format(self.user.get_full_name())

    class Meta:
        ordering = 'blocked', 'user',
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        managed = True


######################################################################################################################


