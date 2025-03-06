from rest_framework import generics
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework.views import Response

from telegram.permissions import TelegramPermission
from .serializers import *


class TGbotUserAPICreateView(generics.CreateAPIView):
    serializer_class = TGbotUserSerializer
    permission_classes = (TelegramPermission,)

    @method_decorator(ratelimit(key='ip', rate='15/m', method='POST'))
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TGbotUserAPIList(generics.ListAPIView):
    permission_classes = (TelegramPermission, )

    @method_decorator(ratelimit(key='ip', rate='15/m', method='GET'))
    def get(self, request, username, *args, **kwargs):
        data = TGbotUser.objects.filter(pk=username)
        return Response({'tg_user': TGbotUserSerializer(data, many=True).data})


class CommentAPICreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (TelegramPermission,)

    @method_decorator(ratelimit(key='ip', rate='15/m', method='POST'))
    def post(self, request, task_id, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentAPIList(generics.ListAPIView):
    permission_classes = (TelegramPermission,)

    @method_decorator(ratelimit(key='ip', rate='15/m', method='GET'))
    def get(self, request, task_id, *args, **kwargs):
        data = Comment.objects.filter(task_id=task_id)
        return Response({'comments': CommentSerializer(data, many=True).data})
