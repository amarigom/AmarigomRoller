"""Estrategias de notificación y factory que elige la implementación según la configuración."""
import logging
from abc import ABC, abstractmethod

from exceptions import ExternalServiceError

logger = logging.getLogger(__name__)


class Notifier(ABC):
    @abstractmethod
    def send(self, subject, html, to):
        """Envía el mensaje; lanza ExternalServiceError si no se pudo."""


class LogNotifier(Notifier):
    """Sin proveedor configurado: deja el mensaje registrado en el log."""

    def send(self, subject, html, to):
        logger.info("Notificación (sin proveedor de correo) para %s: %s", to, subject)


class ResendNotifier(Notifier):
    def __init__(self, api_key, sender):
        self.api_key = api_key
        self.sender = sender

    def send(self, subject, html, to):
        import resend
        resend.api_key = self.api_key
        try:
            resend.Emails.send({"from": self.sender, "to": [to], "subject": subject, "html": html})
        except Exception as e:
            logger.exception("Falló el envío con Resend")
            raise ExternalServiceError("No se pudo enviar la solicitud") from e


def create_notifier(config):
    if config.get('RESEND_API_KEY'):
        return ResendNotifier(config['RESEND_API_KEY'], config.get('MAIL_DEFAULT_SENDER'))
    return LogNotifier()
