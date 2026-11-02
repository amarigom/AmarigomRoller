from datetime import datetime, timezone


def utcnow():
    """Fecha/hora UTC sin zona (como se guarda en las columnas DateTime)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
