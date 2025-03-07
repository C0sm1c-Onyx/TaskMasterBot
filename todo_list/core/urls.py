from django.urls import path
from core.views import (
    TaskAPICreateView, TaskAPIUpdateView, TaskAPIDestroyView,
    CategoryAPIDestroyView, CategoryAPICreateView, CategoryAPIList,
    CategoryAPIUpdateView, TaskAPIList, TGbotUserAPICreateView, TGbotUserAPIList,
    CommentAPICreateView, CommentAPIList
)


urlpatterns = [
    path('api/v1/task-list/<str:user_id>/', TaskAPIList.as_view()),
    path('api/v1/category-list/', CategoryAPIList.as_view()),
    path('api/v1/del-task/<int:pk>/', TaskAPIDestroyView.as_view()),
    path('api/v1/del-category/<int:pk>/', CategoryAPIDestroyView.as_view()),
    path('api/v1/create-task/', TaskAPICreateView.as_view()),
    path('api/v1/create-category/', CategoryAPICreateView.as_view()),
    path('api/v1/update-task/<int:pk>/', TaskAPIUpdateView.as_view()),
    path('api/v1/update-category/<int:pk>/', CategoryAPIUpdateView.as_view()),
    path('api/v1/create_tg_user/', TGbotUserAPICreateView.as_view()),
    path('api/v1/get_user/<str:username>/', TGbotUserAPIList.as_view()),
    path('api/v1/create_comment/<int:task_id>/', CommentAPICreateView.as_view()),
    path('api/v1/list-comment/<int:task_id>/', CommentAPIList.as_view())
]