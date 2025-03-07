from core.serializers import TaskSerializer, CategorySerializer, TGbotUserSerializer, CommentSerializer
from core.models import Task, Category
from rest_framework import generics
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework.views import Response
from core.permissions import TelegramPermission
from core.models import TGbotUser, Comment


class TaskAPIList(generics.ListAPIView):
    permission_classes = (TelegramPermission,)

    @method_decorator(ratelimit(key='ip', rate='15/m', method='GET'))
    def get(self, request, user_id, *args, **kwargs):
        data = Task.objects.filter(user=user_id)
        return Response({'Tasks': TaskSerializer(data, many=True).data})


class CategoryAPIList(generics.ListAPIView):
    permission_classes = (TelegramPermission,)

    @method_decorator(ratelimit(key='ip', rate='15/m', method='GET'))
    def get(self, request, *args, **kwargs):
        data = Category.objects.all()
        return Response({'Categories': CategorySerializer(data, many=True).data})


class TaskAPIDestroyView(generics.DestroyAPIView, ):
    permission_classes = (TelegramPermission,)
    serializer_class = TaskSerializer

    @method_decorator(ratelimit(key='ip', rate='15/m', method='DELETE'))
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CategoryAPIDestroyView(generics.DestroyAPIView):
    permission_classes = (TelegramPermission,)
    serializer_class = CategorySerializer

    @method_decorator(ratelimit(key='ip', rate='15/m', method='DELETE'))
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskAPICreateView(generics.CreateAPIView):
    permission_classes = (TelegramPermission,)
    serializer_class = TaskSerializer

    @method_decorator(ratelimit(key='ip', rate='15/m', method='POST'))
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryAPICreateView(generics.CreateAPIView):
    permission_classes = (TelegramPermission,)
    serializer_class = CategorySerializer

    @method_decorator(ratelimit(key='ip', rate='15/m', method='POST'))
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskAPIUpdateView(generics.UpdateAPIView):
    permission_classes = (TelegramPermission,)
    serializer_class = TaskSerializer

    @method_decorator(ratelimit(key='ip', rate='15/m', method='PUT'))
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @method_decorator(ratelimit(key='ip', rate='15/m', method='PATCH'))
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CategoryAPIUpdateView(generics.UpdateAPIView):
    permission_classes = (TelegramPermission,)
    serializer_class = CategorySerializer

    @method_decorator(ratelimit(key='ip', rate='15/m', method='PUT'))
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @method_decorator(ratelimit(key='ip', rate='15/m', method='PATCH'))
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


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

