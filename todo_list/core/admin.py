from django.contrib import admin

from .models import *
from users.models import User


admin.site.register(Task)
admin.site.register(Category)
admin.site.register(User)