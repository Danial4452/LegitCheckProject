from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from .models import User


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')

        try:
            user = User.objects.get(login=login)
        except User.DoesNotExist:
            return Response(
                {'error': 'Неверный логин или пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(password, user.password):
            return Response(
                {'error': 'Неверный логин или пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'message': 'ok',
            'user_id': user.id,
            'role': user.role.name
        })

