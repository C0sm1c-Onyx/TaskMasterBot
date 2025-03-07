from django.http import JsonResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.views import TokenObtainPairView
from auth_users.serializers import CustomTokenObtainPairSerializer

from auth_users.models import AuthUser


def activate_user_email(request, uidb64=None, token=None):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = AuthUser.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.save()
        return JsonResponse({"OK": "Activation done"})
    else:
        return JsonResponse({"error": "Activation failed"})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
