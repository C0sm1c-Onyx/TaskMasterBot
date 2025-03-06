from django.urls import path
from .views import *


urlpatterns = [
    path('api/v1/create_tg_user/', TGbotUserAPICreateView.as_view()),
    path('api/v1/get_user/<str:username>/', TGbotUserAPIList.as_view()),
    path('api/v1/create_comment/<int:task_id>/', CommentAPICreateView.as_view()),
    path('api/v1/list-comment/<int:task_id>/', CommentAPIList.as_view())
]