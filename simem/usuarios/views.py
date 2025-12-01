from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from helpers.responses import ok_response, ok_logout, permission_denied_response

User = get_user_model()


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        permisos = list(user.get_all_permissions())
        grupos = list(user.groups.values_list('name', flat=True))
        nombre_completo = f'{user.first_name} {user.apellido_paterno} {user.apellido_materno}'.strip()

        data = {
            'user_id': user.id,
            'last_login': user.last_login,
            'token': token.key,
            'nombre_completo': nombre_completo,
            'first_name': user.first_name,
            'apellido_paterno': user.apellido_paterno,
            'apellido_materno': user.apellido_materno,
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'grupos': grupos,
            'permisos': permisos,
        }
        user.last_login = timezone.now()
        user.save()
        return ok_response(data)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        Token.objects.filter(user=user).delete()
        return ok_logout(None)