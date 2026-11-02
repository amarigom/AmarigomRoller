from datetime import datetime, timedelta, timezone

import jwt

from exceptions import AuthenticationError

ALGORITHM = 'HS256'


class TokenService:
    def __init__(self, secret_key, expires_minutes):
        self.secret_key = secret_key
        self.expires_minutes = expires_minutes

    @property
    def expires_in(self):
        return self.expires_minutes * 60

    def issue(self, user):
        ahora = datetime.now(timezone.utc)
        payload = {
            'sub': str(user.id),
            'iat': ahora,
            'exp': ahora + timedelta(minutes=self.expires_minutes),
        }
        return jwt.encode(payload, self.secret_key, algorithm=ALGORITHM)

    def decode(self, token):
        """Devuelve el id de usuario del token o lanza AuthenticationError."""
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[ALGORITHM],
                options={'require': ['exp', 'sub']},
            )
            return int(payload['sub'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("La sesión expiró, iniciá sesión nuevamente")
        except (jwt.InvalidTokenError, ValueError):
            raise AuthenticationError("Token inválido")
