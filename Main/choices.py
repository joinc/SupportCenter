# -*- coding: utf-8 -*-

######################################################################################################################


SELECT_SIGNATURE_CHOICES = (
    (0, 'Новый'),
    (1, 'Продление')
)


######################################################################################################################


STATUS_SIGNATURE_CHOICES = (
    (0, 'Действующие'),
    (1, 'Продленные'),
    (2, 'Истекшие'),
    (3, 'Аннулированные')
)


######################################################################################################################


CATEGORY_PERMISSION = (
    (0, 'Настройки системы'),
    (1, 'Пользователи'),
    (2, 'Организации'),
    (3, 'Электронные подписи'),
    (4, 'Инциденты'),
)


######################################################################################################################


"""

"""
FULL_MENU = (
    (
        ('configure_edit', ),
        'configure_list',
        'Настройки',
        'fas fa-cogs',
    ),
    (
        ('profile_list', 'profile_edit', ),
        'profile_list',
        'Пользователи',
        'fas fa-user-friends',
    ),
    (
        ('organization_list', 'organization_edit', ),
        'organization_list',
        'Организации',
        'fas fa-sitemap',
    ),
    (
        ('signature_list', 'signature_edit', 'signature_moderator', ),
        'signature_list',
        'Подписи',
        'fas fa-file-contract',
    ),
    (
        ('violation_list', 'violation_edit', 'violation_moderator', ),
        'violation_list',
        'Инциденты',
        'fab fa-galactic-republic',
    ),
)


######################################################################################################################