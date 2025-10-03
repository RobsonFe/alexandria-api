from django.core.files.storage import FileSystemStorage
from django.conf import settings
from accounts.models import User
import uuid
import os

class UserService:
    """Camada de serviço para operações do usuário."""

    def update_avatar(self, user: User, avatar) -> User:
        """Atualiza avatar se arquivo for enviado. Retorna user modificado (não salva)."""
        if not avatar:
            return user

        storage = FileSystemStorage(
            location=os.path.join(settings.MEDIA_ROOT, 'avatars'),
            base_url=f"{settings.MEDIA_URL}avatars/"
        )

        if user.avatar and user.avatar not in ("/media/avatars/default.png", "avatars/default.png"):
            old = user.avatar.replace(settings.MEDIA_URL, "") if user.avatar.startswith(settings.MEDIA_URL) else user.avatar.lstrip('/')
            if storage.exists(old):
                storage.delete(old)

        extension = avatar.name.rsplit('.', 1)[-1].lower()
        filename = f"{uuid.uuid4()}.{extension}"
        file_path = storage.save(filename, avatar) 
        user.avatar = storage.base_url + os.path.basename(file_path)
        return user