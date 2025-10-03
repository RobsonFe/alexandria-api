# Auth (Autenticação e Sessões)

## Visão Geral
O app `auth` gerencia o ciclo de vida de autenticação via JWT (SimpleJWT):

- Registro de usuário (`POST /auth/signup`)
- Login e emissão de tokens (`POST /auth/login`)
- Logout (blacklist de refresh token) (`POST /auth/logout`)

Tokens emitidos:
- Access Token: curto prazo (ex: 5–15 min conforme configuração).
- Refresh Token: usado para renovar access; é invalidado (blacklist) no logout.

## Arquitetura
1. Views (`SignInView`, `SignUpView`, `SignOutView`) recebem e validam payload.
2. Mixin de validação (`SiginValidationMixin`) faz validações básicas de campos obrigatórios.
3. Service (`AuthenticationService`) encapsula lógica de obtenção e criação de usuários.
4. Serialização de usuário de saída reutiliza `accounts.UserSerializer`.

## Endpoints
| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| POST | `/auth/login` | Público | Autentica e retorna tokens |
| POST | `/auth/signup` | Público | Cria novo usuário e retorna tokens |
| POST | `/auth/logout` | Bearer (Access) | Invalida (blacklist) refresh token |

### POST /auth/login
Body JSON:
```json
{ "email": "john@example.com", "password": "Senha123" }
```
Resposta (200):
```json
{ "access": "<jwt_access>", "refresh": "<jwt_refresh>" }
```
Erros comuns:
- 400: Campos ausentes / credenciais inválidas (tratado como `AuthenticationFailed` em camadas posteriores caso melhore a validação)

Fluxo interno:
1. `SignInView.post` → `validate_sigin(data)` (verifica email e password presentes)
2. Chama `AuthenticationService.signin` (busca user e confere senha com `check_password`).
3. Gera RefreshToken (`RefreshToken.for_user`).
4. Retorna par de tokens.

### POST /auth/signup
Body JSON:
```json
{ "name": "John", "email": "john@example.com", "password": "Senha123" }
```
Resposta (200):
```json
{
	"result": {
		"user": { "id": 1, "email": "john@example.com", "name": "John", "avatar": "https://api.suaapp.com/avatars/default.png" },
		"access": "<jwt_access>",
		"refresh": "<jwt_refresh>"
	}
}
```
Fluxo:
1. `SignUpView.post` → `validate_signup(data)`.
2. `AuthenticationService.signup` cria usuário (checando duplicidade de email).
3. Serializer `UserSerializer` monta resposta.
4. Gera tokens para login automático pós-registro.

### POST /auth/logout
Body JSON:
```json
{ "refresh": "<jwt_refresh>" }
```
Resposta (205 Reset Content): sem body.

Fluxo:
1. `SignOutView.post` exige autenticação (Access válido).
2. Recupera `refresh` do body.
3. Constrói `RefreshToken(refresh)` e chama `blacklist()`.
4. Retorna 205.

## Service: AuthenticationService
### `signin(data)`
- Busca usuário por email.
- Valida senha com `check_password`.
- Retorna instância de usuário ou `None`.

### `signup(data)`
- Verifica se email já existe.
- Usa `User.objects.create_user` (aplica `set_password`).
- Retorna novo usuário ou `None` (se duplicado ou erro genérico).

## Validação (SiginValidationMixin)
Métodos:
- `validate_sigin` → exige `email` e `password`.
- `validate_signup` → exige `name`, `email`, `password`.

Observação: ambos retornam `(True, None)` mas poderiam ser refatorados para apenas lançar `ValidationError` para consistência (como feito em `accounts`).

## Integração com Accounts
1. Usuário se registra ou faz login aqui.
2. Usa `access` token para acessar `/accounts/user`.
3. Atualização de perfil (nome, senha, avatar) é responsabilidade do app `accounts`.

## Erros e Considerações
| Situação | Melhor Tratamento Futuro |
|----------|--------------------------|
| Login com credenciais inválidas retorna tokens vazios ou falha silenciosa | Retornar 401 com mensagem clara |
| Retorno `None` em service sem exceção | Substituir por exceções semânticas |
| Falta de limitação de tentativas | Implementar throttling (DRF throttle ou Redis) |

## Melhorias Sugeridas
- Unificar padrão de validação (raise-only).
- Adicionar confirmação de senha no signup.
- Implementar endpoint de refresh separado (se não existir já na configuração padrão do SimpleJWT `/api/token/refresh/`).
- Adicionar verificação de e-mail (email verification flow) e recuperação de senha.

## Referências de Código
- Views: `auth/views.py` (`SignInView`, `SignUpView`, `SignOutView`)
- Service: `auth/service/services.py` (`AuthenticationService`)
- Validators: `auth/validations/validation.py` (`SiginValidationMixin`)
- Model de usuário: está em `accounts.models.User` (compartilhado)

## Fluxo Resumido (Login)
```
Client -> POST /auth/login {email, password}
	-> View valida campos
	-> Service verifica credenciais
	-> Gera tokens (access + refresh)
	<- 200 {access, refresh}
```

## Checklist Rápido
1. Criar usuário: `POST /auth/signup`
2. Login: `POST /auth/login`
3. Salvar tokens (access/refresh)
4. Usar `Authorization: Bearer <access>` no app `accounts`
5. Logout: `POST /auth/logout` com refresh

---
Esta documentação acelera onboarding no módulo de autenticação.
