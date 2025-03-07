from rest_framework import serializers

from core.models import Category, Task
from auth_users.models import AuthUser
from core.models import TGbotUser, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('id', 'username', 'email')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_id', 'category_name')


class TaskSerializer(serializers.ModelSerializer):
    task_category_id = serializers.CharField(required=True)
    user_id = serializers.CharField(required=True)

    class Meta:
        model = Task
        fields = ('user_id', 'task_id', 'task_title', 'task_description', 'start_date', 'task_category_id', 'create_data')


class TGbotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TGbotUser
        fields = ('username_id', 'chat_id')


class CommentSerializer(serializers.ModelSerializer):
    username_id = serializers.CharField(required=True)
    task_id = serializers.CharField(required=True)

    class Meta:
        model = Comment
        fields = ('comment_id', 'comment', 'username_id', 'task_id')
