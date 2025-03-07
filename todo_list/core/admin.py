from django.contrib import admin

from auth_users.models import AuthUser


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name')
    list_display_links = ('category_id', 'category_name')
    search_fields = ('category_name',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_title', 'task_description', 'start_date', 'user_id')
    list_display_links = ('task_id', 'task_title', 'task_description', 'start_date', 'user_id')
    search_fields = ('task_title',)


class AuthAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_verified')
    list_display_links = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_verified')
    search_fields = ('username',)


def register_models():
    from core.models import Task, Category

    admin.site.register(Task, TaskAdmin)
    admin.site.register(Category, CategoryAdmin)
    admin.site.register(AuthUser, AuthAdmin)

    admin.site.site_title = 'Aдмин-панель TaskMasterBot'


register_models()

