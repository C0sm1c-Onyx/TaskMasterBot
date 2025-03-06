from django.db import models
from django.contrib.auth.models import AbstractUser

from auth_users.managers import UserManager


class AuthUser(AbstractUser):
    username = models.CharField('username', max_length=16, unique=True)
    email = models.CharField('email', max_length=30, unique=True)
    date_joined = models.DateTimeField('date_joined', auto_now_add=True)
    is_active = models.BooleanField('is_active', default=False)
    is_staff = models.BooleanField('is_staff', default=False)
    is_verified = models.BooleanField('is_verified', default=False)

    object = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        verbose_name = 'auth_user'
        verbose_name_plural = 'auth_users'
        unique_together = ('username', 'email')

        swappable = "AUTH_USER_MODEL"
