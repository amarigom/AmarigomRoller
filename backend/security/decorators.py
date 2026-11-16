from functools import wraps

from flask import current_app, g, request

import container
from exceptions import AuthenticationError, PermissionDenied
from security.permissions import has_permission


def _bearer_token():
    cabecera = request.headers.get('Authorization', '')
    esquema, _, token = cabecera.partition(' ')
    if esquema.lower() != 'bearer' or not token.strip():
        raise AuthenticationError("Falta iniciar sesión")
    return token.strip()


def authenticate():
    """Carga g.current_user desde el token. El rol y el estado se leen de la base en cada pedido."""
    user = container.auth_service().user_from_token(_bearer_token())
    g.current_user = user
    return user


def auth_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        authenticate()
        return view(*args, **kwargs)
    return wrapper


def permission_required(permission):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            user = authenticate()
            if not has_permission(user.rol, permission):
                current_app.logger.warning(
                    "Acceso denegado: usuario %s (%s) sin permiso %s", user.id, user.rol, permission)
                raise PermissionDenied()
            return view(*args, **kwargs)
        return wrapper
    return decorator
