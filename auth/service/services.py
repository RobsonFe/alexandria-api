from django.contrib.auth.hashers import check_password
from accounts.models import User


class AuthenticationService:
    """
    Serviço responsável pela autenticação de usuários
    """
    
    def signin(self, data):
        """
        Realiza o login do usuário
        """
        email = data.get("email")
        password = data.get("password")
        
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return user
            return None
        except User.DoesNotExist:
            return None
    
    def signup(self, data):
        """
        Realiza o cadastro do usuário
        """
        
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        
        try:
            if User.objects.filter(email=email).exists():
                return None
            
            user = User.objects.create_user(
                name=name,
                email=email,
                password=password
            )
            return user
        except Exception:
            return None