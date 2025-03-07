from django.urls import path
from auth_users.views import activate_user_email


urlpatterns = [
    path('auth_users/verify/<str:uidb64>/<str:token>/', activate_user_email),
]