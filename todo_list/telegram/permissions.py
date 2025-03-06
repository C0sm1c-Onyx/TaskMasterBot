from rest_framework import permissions


class TelegramPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'TelegramBot' in request.headers.get('User-Agent'):
            return True

        return request.user.is_authenticated