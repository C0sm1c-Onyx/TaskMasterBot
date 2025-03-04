from rest_framework import generics
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from .serializers import *
from .models import *


class TaskAPIList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )

    @method_decorator(ratelimit(key='ip', rate='15/m', method='GET'))
    def get(self, request, *args, **kwargs):
        data = Task.objects.all()
        return Response({'Tasks': TaskSerializer(data, many=True).data})


class CategoryAPIList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )

    @method_decorator(ratelimit(key='ip', rate='15/m', method='GET'))
    def get(self, request, *args, **kwargs):
        data = Category.objects.all()
        return Response({'Categories': CategorySerializer(data, many=True).data})


class TaskAPIDestroyView(generics.DestroyAPIView, ):
    permission_classes = (IsAuthenticated, )
    serializer_class = TaskSerializer

    @method_decorator(ratelimit(key='ip', rate='15/m', method='DELETE'))
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CategoryAPIDestroyView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer

    @method_decorator(ratelimit(key='ip', rate='15/m', method='DELETE'))
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskAPICreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = TaskSerializer

    @method_decorator(ratelimit(key='ip', rate='15/m', method='POST'))
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryAPICreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer

    @method_decorator(ratelimit(key='ip', rate='15/m', method='POST'))
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskAPIUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = TaskSerializer

    @method_decorator(ratelimit(key='ip', rate='15/m', method='PUT'))
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @method_decorator(ratelimit(key='ip', rate='15/m', method='PATCH'))
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CategoryAPIUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer

    @method_decorator(ratelimit(key='ip', rate='15/m', method='PUT'))
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @method_decorator(ratelimit(key='ip', rate='15/m', method='PATCH'))
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

