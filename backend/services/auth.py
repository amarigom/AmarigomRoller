from datetime import timedelta

from werkzeug.security import check_password_hash, generate_password_hash

from exceptions import AuthenticationError, TooManyAttempts
from repositories.user import UserRepository
from schemas.auth import TokenOut, UserOut
from security.permissions import permissions_for
from utils.clock import utcnow

# Se compara contra este hash cuando el email no existe, para que la demora no revele qué cuentas hay
_DUMMY_HASH = generate_password_hash("contraseña-inexistente")


class AuthService:
    def __init__(self, users, tokens, max_attempts, lock_minutes):
        self.users = users
        self.tokens = tokens
        self.max_attempts = max_attempts
        self.lock_minutes = lock_minutes

    def login(self, email, password):
        user = self.users.get_by_email(email)
        if user is None:
            check_password_hash(_DUMMY_HASH, password)
            raise AuthenticationError()

        ahora = utcnow()
        if user.bloqueado_hasta and user.bloqueado_hasta > ahora:
            raise TooManyAttempts()

        if not check_password_hash(user.password_hash, password) or not user.activo:
            self._register_failure(user, ahora)
            raise AuthenticationError()

        user.intentos_fallidos = 0
        user.bloqueado_hasta = None
        user.ultimo_login = ahora
        self.users.commit()
        return self.token_response(user)

    def _register_failure(self, user, ahora):
        user.intentos_fallidos = (user.intentos_fallidos or 0) + 1
        if user.intentos_fallidos >= self.max_attempts:
            user.bloqueado_hasta = ahora + timedelta(minutes=self.lock_minutes)
            user.intentos_fallidos = 0
        self.users.commit()

    def token_response(self, user):
        return TokenOut(
            token=self.tokens.issue(user),
            expires_in=self.tokens.expires_in,
            user=UserOut.from_model(user),
            permissions=sorted(permissions_for(user.rol)),
        )

    def user_from_token(self, token):
        """El usuario se relee de la base: un rol cambiado o una cuenta desactivada aplican de inmediato."""
        user = self.users.get(self.tokens.decode(token))
        if user is None or not user.activo:
            raise AuthenticationError("Sesión inválida")
        return user

    def change_password(self, user, actual, nueva):
        if not check_password_hash(user.password_hash, actual):
            raise AuthenticationError("La contraseña actual no es correcta")
        user.password_hash = generate_password_hash(nueva)
        self.users.commit()
