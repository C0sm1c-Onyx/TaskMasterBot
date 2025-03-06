from django.urls import path
from .views import *


urlpatterns = [
    path('auth_users/verify/<str:uidb64>/<str:token>/', activate_user_email),
]