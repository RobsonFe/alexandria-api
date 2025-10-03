from auth.types.type import SiginDataType, UserDataType
from core.exceptions import ValidationError


class SiginValidationMixin:
  """
  Mixin para validação de dados de login.
  """
  def validate_sigin(self, data:SiginDataType) -> bool | ValidationError:
    """Função para validar dados de login.

    Args:
        data (SiginDataType): Dados de login.

    Raises:
        ValidationError: Se os dados forem inválidos.

    Returns:
        bool | ValidationError: True se os dados forem válidos, caso contrário lança ValidationError.
    """
    if not data.get("email") or not data.get("password"):
        raise ValidationError("Email e senha são obrigatórios.")
    return True, None
    
  def validate_signup(self, data:UserDataType) -> bool | ValidationError:
    """Função para validar dados de registro.

    Args:
        data (UserDataType): Dados de registro.

    Raises:
        ValidationError: Se os dados forem inválidos.

    Returns:
        bool | ValidationError: True se os dados forem válidos, caso contrário lança ValidationError.
    """
    if not data.get("name") or not data.get("email") or not data.get("password"):
          raise ValidationError("Nome, email e senha são obrigatórios.")
    return True, None