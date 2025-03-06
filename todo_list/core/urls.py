from django.urls import path
from .views import *


urlpatterns = [
    path('api/v1/task-list/<str:user_id>/', TaskAPIList.as_view()),
    path('api/v1/category-list/', CategoryAPIList.as_view()),
    path('api/v1/del-task/<int:pk>/', TaskAPIDestroyView.as_view()),
    path('api/v1/del-category/<int:pk>/', CategoryAPIDestroyView.as_view()),
    path('api/v1/create-task/', TaskAPICreateView.as_view()),
    path('api/v1/create-category/', CategoryAPICreateView.as_view()),
    path('api/v1/update-task/<int:pk>/', TaskAPIUpdateView.as_view()),
    path('api/v1/update-category/<int:pk>/', CategoryAPIUpdateView.as_view()),
]