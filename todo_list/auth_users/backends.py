from auth_users.models import AuthUser
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
            return AuthUser.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None

    def authenticate(self, request, username, email, password):
        try:
            user = AuthUser.objects.get(
                Q(username=username) & Q(email=email)
            )
        except ObjectDoesNotExist:
            return None

        return user if user.check_password(password) else None
