from rest_framework import permissions


class TelegramPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
        if 'User-Agent' in request.META:
            return True
            if 'TelegramBot' in request.META['User-Agent']:
                return True

        return request.user.is_authenticated