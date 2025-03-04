from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.mixins import PermissionRequiredMixin

from users.managers import UserManager


class User(AbstractBaseUser, PermissionRequiredMixin):
    username = models.CharField('username', max_length=16)
    email = models.CharField('email', max_length=30, unique=True)
    date_joined = models.DateTimeField('date_joined', auto_now_add=True)
    is_active = models.BooleanField('is_active', default=False)
    is_staff = models.BooleanField('is_staff', default=False)
    is_verified = models.BooleanField('is_verified', default=False)

    object = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = ('users',)
        verbose_name_plural = ('users',)
        unique_together = ('username', 'email')
