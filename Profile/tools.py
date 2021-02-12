# -*- coding: utf-8 -*-

from Profile.models import UserProfile

######################################################################################################################


def check_password(username, password1, password2):
    """
    Проверка выполнения требований к паролю
    :param username:
    :param password1:
    :param password2:
    :return:
    """
    message_list = []
    if password1 != password2:
        message_list.append('Пароли не совпадают.')
    if len(password1) < 8:
        message_list.append('Длина пароля менее 8 символов.')
    if password1.isdigit():
        message_list.append('Пароль состоит только из цифр.')
    if password1 == username:
        message_list.append('Пароль совпадает с логином.')
    return message_list


######################################################################################################################


def get_list_profile(username='', organization=0):
    """
    Получение количества и списка пользователей по заданным критериям поиска
    :param username:
    :param organization:
    :return:
    """
    if username:
        if organization:
            # Когда идет поиск по имени пользователя и выбрана организация
            total_profile = UserProfile.objects.filter(
                user__username__contains=username,
                organization=organization,
            ).count()
            if total_profile < 20:
                list_profile = list(
                    UserProfile.objects.filter(
                        user__username__contains=username,
                        organization=organization,
                    )[:total_profile]
                )
                list_profile.extend(
                    UserProfile.objects.filter(
                        user__last_name__contains=username,
                        organization=organization,
                    )[:20 - total_profile]
                )
            else:
                list_profile = UserProfile.objects.filter(
                    user__username__contains=username,
                )[:20]
            total_profile = total_profile + UserProfile.objects.filter(
                user__last_name__contains=username,
                organization=organization,
            ).count()

        else:
            # Когда идет поиск только по имени пользователя
            total_profile = UserProfile.objects.filter(
                user__username__contains=username,
            ).count()
            if total_profile < 20:
                list_profile = list(
                    UserProfile.objects.filter(
                        user__username__contains=username,
                    )[:20]
                )
                list_profile.extend(
                    UserProfile.objects.filter(
                        user__last_name__contains=username,
                    )[:20 - total_profile]
                )
            else:
                list_profile = UserProfile.objects.filter(
                    user__username__contains=username,
                )[:20]
            total_profile = total_profile + UserProfile.objects.filter(
                user__last_name__contains=username,
            ).count()
    else:
        if organization:
            # Когда идет поиск только по организации
            total_profile = UserProfile.objects.filter(
                organization=organization,
            ).count()
            list_profile = UserProfile.objects.filter(
                organization=organization,
            )[:20]
        else:
            # Когда идет поиск с пустым запросом (без имени и организации)
            total_profile = UserProfile.objects.all().count()
            list_profile = UserProfile.objects.all()[:20]
    return [total_profile, list_profile]


######################################################################################################################
