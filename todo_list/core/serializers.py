from rest_framework import serializers
from .models import Category, Task
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Task
        fields = ('user', 'task_id', 'task_title', 'task_description', 'category', 'start_date')


class CategorySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ('category_id', 'category_name', 'tasks')
