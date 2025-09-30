from rest_framework.exceptions import AuthenticationFailed
from django.core.files.storage import FileSystemStorage
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import User
from django.conf import settings
import uuid
import os

class UserView(APIView):

    def get(self, request):
        user = request.user

        User.objects.filter(id=user.id)

        if not user:
            raise AuthenticationFailed(
                "Usuário não autenticado.", code=status.HTTP_401_UNAUTHORIZED
            )

        user_data = UserSerializer(user).data

        return Response({"result": user_data}, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user

        if not user:
            raise AuthenticationFailed(
                "Usuário não autenticado.", code=status.HTTP_401_UNAUTHORIZED
            )

        name = request.data.get("name", user.name)
        email = request.data.get("email", user.email)
        password = request.data.get("password")
        avatar = request.FILES.get("avatar")

        user.name = name
        user.email = email
        
        if password:
            user.set_password(password)

        storage = FileSystemStorage(
            location=os.path.join(settings.MEDIA_ROOT, 'avatars'),
            base_url=f"{settings.MEDIA_URL}avatars/"
        )

        if avatar:
            content_type = avatar.content_type
            extension = avatar.name.split(".")[-1]
            if content_type not in ["image/jpeg", "image/png"]:
                raise ValidationError(
                    "Formato de imagem inválido. Use JPEG ou PNG.",
                    code=status.HTTP_400_BAD_REQUEST,
                )
            if extension not in ["jpg", "jpeg", "png"]:
                raise ValidationError(
                    "Extensão de imagem inválida. Use .jpg, .jpeg ou .png.",
                    code=status.HTTP_400_BAD_REQUEST,
                )
            
            if user.avatar and user.avatar != "/media/avatars/default.png":
                old_file_path = user.avatar.replace(settings.MEDIA_URL, "")
                if storage.exists(old_file_path):
                    storage.delete(old_file_path)
            
            filename = f"{uuid.uuid4()}.{extension}"
            file_path = storage.save(filename, avatar)
            user.avatar = storage.url(file_path)

        user.save()

        user_data = UserSerializer(user).data

        return Response({"result": user_data}, status=status.HTTP_200_OK)