from rest_framework import serializers
from .models import Category, Task
from auth_users.models import AuthUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('id', 'username', 'email')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_id', 'category_name')


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task_category = CategorySerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('user', 'task_id', 'task_title', 'task_description', 'start_date', 'task_category')