from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from auth.validations.validation import SiginValidationMixin
from rest_framework.views import APIView
from .service.services import AuthenticationService
from rest_framework import status

class SignInView(SiginValidationMixin,APIView):

    permission_classes = [AllowAny]
    
    def __init__(self, service=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service or AuthenticationService()

    def post(self, request):
        
        data = request.data

        is_valid, error_response = self.validate_sigin(data)
        
        if not is_valid:
            raise error_response
        
        signin = self.service.signin(data)
            
        refresh = RefreshToken.for_user(signin)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class SignUpView(SiginValidationMixin,APIView):

    permission_classes = [AllowAny]
    
    def __init__(self, service=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service or AuthenticationService()

    def post(self, request):

        data = request.data

        is_valid, error_response = self.validate_signup(data)
        if not is_valid:
            raise error_response
        
        singup = self.service.signup(data)

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
            user.save()
            token.blacklist()
        except TokenError:
            raise AuthenticationFailed(
                "Erro ao invalidar o token.", code=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            status=status.HTTP_205_RESET_CONTENT
        )