"""Excepciones de dominio: las capas internas las lanzan y routes/errors.py las traduce a HTTP."""


class AppError(Exception):
    status_code = 500
    default_message = "Error interno"

    def __init__(self, message=None, detalles=None):
        self.message = message or self.default_message
        self.detalles = detalles or []
        super().__init__(self.message)


class ValidationFailed(AppError):
    status_code = 400
    default_message = "Datos inválidos"


class AuthenticationError(AppError):
    status_code = 401
    default_message = "Credenciales inválidas"


class PermissionDenied(AppError):
    status_code = 403
    default_message = "No tenés permisos para realizar esta acción"


class NotFoundError(AppError):
    status_code = 404
    default_message = "Recurso no encontrado"


class ConflictError(AppError):
    status_code = 409
    default_message = "El recurso entra en conflicto con datos existentes"


class UnprocessableError(AppError):
    status_code = 422
    default_message = "No se pudo procesar la solicitud"


class TooManyAttempts(AppError):
    status_code = 429
    default_message = "Demasiados intentos. Probá nuevamente más tarde"


class ExternalServiceError(AppError):
    status_code = 502
    default_message = "Falló un servicio externo"
