from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from core.exceptions import ValidationError
from rest_framework.views import APIView
from accounts.auth import AuthenticationService
from django.utils.timezone import now
from rest_framework import status

class SignInView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        auth_service = AuthenticationService()
        signin = auth_service.signin(email, password)

        if not signin:
            raise AuthenticationFailed(
                "Credenciais inválidas.", code=status.HTTP_401_UNAUTHORIZED
            )

        user = UserSerializer(signin).data
        
        if not user:
            raise AuthenticationFailed(
                "Erro na autenticação.", code=status.HTTP_400_BAD_REQUEST
            )
            
        refresh = RefreshToken.for_user(signin)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class SignUpView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        if not name or not email or not password:
            raise ValidationError(
                "Todos os campos são obrigatórios.", code=status.HTTP_400_BAD_REQUEST
            )

        auth_service = AuthenticationService()
        singup = auth_service.signup(name, email, password)

        if not singup:
            raise AuthenticationFailed(
                "Erro ao registrar.", code=status.HTTP_400_BAD_REQUEST
            )

        user = UserSerializer(singup).data
        refresh = RefreshToken.for_user(singup)

        return Response(
            {
                "result": {
                    "user": user,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            },
            status=status.HTTP_200_OK,
        )


class SignOutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        refresh_token = request.data.get("refresh")
        user = request.user
        

        if not refresh_token:
            raise AuthenticationFailed(
                "Token de atualização não fornecido.", code=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            user.last_access = now()
            user.save()
            token.blacklist()
        except TokenError:
            raise AuthenticationFailed(
                "Erro ao invalidar o token.", code=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            status=status.HTTP_205_RESET_CONTENT
        )