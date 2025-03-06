from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username=None, email=None, password=None, **kwargs):
        if not username or not email:
            raise ValueError('The given username and phone must be set')

        if kwargs.get('is_superuser'):
            user = self.model(
                username=username,
                **kwargs
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_active', False)

        return self._create_user(
            username=username, phone=email, password=password, **kwargs
        )

    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)

        return self._create_user(
            username=username, password=password, **kwargs
        )