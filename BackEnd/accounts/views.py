from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import check_password
from .models import User, Token, Role

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        login = request.data.get('username') or request.data.get('login')
        password = request.data.get('password')

        if not login or not password:
            return Response({'error': 'Логин и пароль обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(login=login).exists():
            return Response({'error': 'Пользователь с таким логином уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create default role
        role, _ = Role.objects.get_or_create(name='Expert')

        user = User(login=login, role=role)
        user.set_password(password)
        user.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'Успешно зарегистрировано',
            'token': token.key,
            'user_id': user.id,
            'role': user.role.name
        }, status=status.HTTP_201_CREATED)

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

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'ok',
            'token': token.key,
            'user_id': user.id,
            'role': user.role.name if user.role else None
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
