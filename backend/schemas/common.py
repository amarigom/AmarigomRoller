from pydantic import ValidationError

from exceptions import ValidationFailed


def parse_payload(schema, payload):
    """Valida un payload con un esquema pydantic y traduce los errores a ValidationFailed."""
    try:
        return schema.model_validate(payload if payload is not None else {})
    except ValidationError as e:
        detalles = [
            f"{'.'.join(str(p) for p in err['loc'])}: {err['msg']}".lstrip(': ')
            for err in e.errors()
        ]
        raise ValidationFailed(detalles=detalles)
