from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class keys(models.Model):
    keys_user = models.ForeignKey(User, unique=True, default="", on_delete=models.CASCADE, related_name='Юзер')
    open_key = models.CharField(max_length=210, null=True, blank=True, default='0', verbose_name='Открытый ключ')
    secret_key = models.CharField(max_length=210, null=True, blank=True, default='0', verbose_name='Секретный ключ')


class message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Отправитель')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Получатель')
    text = models.CharField(max_length=200, verbose_name='Сообщение')
    date = models.DateTimeField(default=timezone.now)


class friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Пользователь')
    users_friend = models.ForeignKey(User, unique=True, on_delete=models.CASCADE, related_name='Друг')

    def __str__(self):
        return str(self.users_friend)
