from django.contrib import admin

from .models import *
from auth_users.models import AuthUser


admin.site.register(Task)
admin.site.register(Category)
admin.site.register(AuthUser)