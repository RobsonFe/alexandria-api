# Accounts (Perfil do Usuário)

## Visão Geral
O app `accounts` concentra recursos relacionados ao perfil do usuário autenticado:

- Consulta dos dados do próprio usuário (`GET /accounts/user`)
- Atualização parcial de perfil e troca de senha (`PATCH /accounts/user`)
- Atualização/Upload de avatar (na mesma rota PATCH enviando `multipart/form-data`)

Arquitetura em camadas:
1. View (`UserView`): orquestra requisição e resposta.
2. Serializers: validação e (de)serialização de dados de entrada/saída.
3. Service (`UserService`): regras específicas de manipulação de avatar (arquivo + limpeza do antigo).
4. Validators (`UserValidatorMixin`): validações auxiliares (autenticação e arquivo de imagem) – apenas lançam exceções.
5. Model (`User`): Representa o usuário, agora com `ImageField` para avatar.

## Stack Principal
- Django 5 / DRF
- SimpleJWT (tokens gerados no app `auth`)
- Pillow (suporte ao `ImageField` e processamento futuro de imagens)

## Modelo `User`
Campos relevantes:
- `email` (login, único)
- `name`
- `avatar` (`ImageField(upload_to='avatars/', default='avatars/default.png')`)
- `is_superuser` (também usado como `is_staff` via property)

## Endpoints
| Método | Rota | Autenticação | Descrição |
|--------|------|--------------|-----------|
| GET | `/accounts/user` | Bearer (JWT Access) | Retorna dados do usuário logado |
| PATCH | `/accounts/user` | Bearer (JWT Access) | Atualiza nome, email, senha e opcionalmente avatar |

### GET /accounts/user
Resposta (200):
```json
{
	"result": {
		"id": 1,
		"email": "john@example.com",
		"name": "John",
		"avatar": "https://api.suaapp.com/avatars/abcd1234.jpg"
	}
}
```

### PATCH /accounts/user
Tipos de conteúdo aceitos:
- `application/json` (sem avatar)
- `multipart/form-data` (com avatar)

Campos aceitos (todos opcionais):
- `name`
- `email` (único; validado para não colidir com outro usuário)
- `password` (se enviado, é aplicado com `set_password`)
- `avatar` (arquivo de imagem: JPEG ou PNG)

Exemplo (JSON simples):
```http
PATCH /accounts/user
Authorization: Bearer <token>
Content-Type: application/json

{
	"name": "Novo Nome"
}
```

Exemplo (multipart com avatar e senha):
```
PATCH /accounts/user HTTP/1.1
Authorization: Bearer <token>
Content-Type: multipart/form-data; boundary=XYZ

--XYZ
Content-Disposition: form-data; name="name"

Alice
--XYZ
Content-Disposition: form-data; name="password"

NovaSenhaSegura123
--XYZ
Content-Disposition: form-data; name="avatar"; filename="foto.png"
Content-Type: image/png

<binário>
--XYZ--
```

Resposta (200):
```json
{
	"result": {
		"id": 1,
		"email": "john@example.com",
		"name": "Alice",
		"avatar": "https://api.suaapp.com/avatars/8f3c4b2e.png"
	}
}
```

## Fluxo Interno (PATCH)
1. `UserView.patch` recebe request.
2. Garante autenticação (`permission_classes = [IsAuthenticated]`).
3. Instancia `UserUpdateSerializer(user, data=request.data, partial=True)`.
4. Valida email único e campos básicos.
5. Salva mudanças (inclui `set_password` se `password` veio).
6. Se `avatar` presente:
	 - `validate_avatar_file()` checa MIME e extensão.
	 - `UserService.update_avatar` remove avatar antigo (se não for o default) e salva o novo.
7. Serializa com `UserSerializer` (monta URL absoluta usando `settings.CURRENT_URL`).
8. Retorna `{"result": <dados>}`.

## Validações de Avatar
- Content-Type permitido: `image/jpeg`, `image/png`.
- Extensões permitidas: `.jpg`, `.jpeg`, `.png`.
- Avatar anterior removido se não for o default.

## Possíveis Erros
| Código | Causa |
|--------|-------|
| 401 | Sem token ou token inválido |
| 400 | Email já em uso / formato de imagem inválido |
| 415 | (Opcional futuro) Tipo de mídia não suportado |

## Extensões Futuras Sugeridas
- Redimensionar avatar (thumbnail 256x256) via Pillow.
- Limite de tamanho (ex: 2MB). 
- Auditoria de mudanças de email.
- Endpoint separado para alteração de senha.

## Referências de Código
- View: `accounts/views.py` (`UserView`)
- Serializers: `accounts/serializers.py` (`UserSerializer`, `UserUpdateSerializer`)
- Service: `accounts/service/service.py` (`UserService.update_avatar`)
- Validations: `accounts/validations/validation.py` (`UserValidatorMixin`)
- Model: `accounts/models.py` (`User`)

## Checklist Rápido para Novos Devs
1. Criar usuário via `/auth/signup` (app auth).
2. Obter token via `/auth/login`.
3. Chamar `GET /accounts/user` para ver perfil.
4. Atualizar nome/senha/avatar via `PATCH /accounts/user`.

---
Esta documentação destina-se a acelerar o onboarding no módulo de perfil.
