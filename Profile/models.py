from django.db import models
from django.contrib.auth.models import User
from Main.models import Organization

######################################################################################################################


class AccessRole(models.Model):
    title = models.CharField(
        'Название роли',
        max_length=124,
        default='',
    )
    is_sample = models.BooleanField(
        verbose_name="Это шаблом роли",
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
        related_name='Organization',
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
        related_name='AccessRole',
        on_delete=models.SET_NULL,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания учетной записи',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return '{0}'.format(self.user.get_full_name())

    class Meta:
        ordering = 'blocked', 'user',
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        managed = True


######################################################################################################################

