import random

from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

from phonenumber_field.modelfields import PhoneNumberField

from utils.models import TimeStampAbstractModel

from .managers import UserManager


class User(AbstractUser, TimeStampAbstractModel):
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    username = None
    email = models.EmailField(verbose_name='электронная почта', unique=True, blank=False, null=False)
    groups = models.ManyToManyField(Group, related_name='account_users')
    user_permissions = models.ManyToManyField(Permission, related_name='account_users_permissions')

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{str(self.email) or self.first_name}'


def get_expire_date():
    return timezone.now() + timezone.timedelta(minutes=15)


class UserResetPassword(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'Ключ для сброса пароля'
        verbose_name_plural = 'Ключи для сброса пароля'
        ordering = ('-created_at', '-updated_at')

    user = models.OneToOneField('account.User', on_delete=models.CASCADE, verbose_name='пользователь', )
    key = models.PositiveIntegerField('ключ', default=random.randint(1001, 9999), editable=False,)
    expire_date = models.DateTimeField('срок действия', default=get_expire_date)

    def __str__(self):
        return f'{self.user}'

    def is_expired(self):
        return timezone.now() > self.expire_date
