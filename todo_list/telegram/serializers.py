from rest_framework import serializers

from core.models import TGbotUser, Comment


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