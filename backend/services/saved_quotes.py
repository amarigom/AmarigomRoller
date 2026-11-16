import base64
import hashlib
import hmac
import json

from cryptography.fernet import Fernet, InvalidToken
from flask import current_app, g

from exceptions import ValidationFailed
from models import Product, SavedQuote
from repositories.saved_quotes import SavedQuoteRepository


def _cipher():
    key = hmac.new(current_app.config['SECRET_KEY'].encode(), b'presupuesto-congelado-v2', hashlib.sha256).digest()
    return Fernet(base64.urlsafe_b64encode(key))


def token_presupuesto(producto_id, medidas, opciones, resultado):
    producto = SavedQuoteRepository().session.get(Product, producto_id)
    if producto is None:
        raise ValidationFailed('El producto ya no existe')
    datos = {
        'usuario_id': g.current_user.id,
        'producto_id': producto_id,
        'producto_nombre': producto.nombre,
        'ancho_cm': medidas.w,
        'alto_cm': medidas.h,
        'referencia': medidas.referencia,
        'opciones': opciones,
        'resultado': resultado,
    }
    return _cipher().encrypt(json.dumps(datos, ensure_ascii=False).encode('utf-8')).decode('ascii')


def guardar_presupuesto(token):
    try:
        datos = json.loads(_cipher().decrypt(token.encode('utf-8'), ttl=3600))
    except InvalidToken as exc:
        raise ValidationFailed('El cálculo venció o no es válido; volvé a calcularlo') from exc
    if datos['usuario_id'] != g.current_user.id:
        raise ValidationFailed('El cálculo pertenece a otro usuario')
    resultado = datos['resultado']
    registro = SavedQuote(
        producto_id=datos['producto_id'], producto_nombre=datos['producto_nombre'],
        receta_id=resultado['receta_id'], receta_version=resultado['version'],
        ancho_cm=datos['ancho_cm'], alto_cm=datos['alto_cm'], referencia=datos['referencia'],
        opciones=datos['opciones'], resultado=resultado, usuario_id=g.current_user.id,
        usuario_nombre=g.current_user.nombre,
    )
    repo = SavedQuoteRepository()
    repo.session.add(registro)
    repo.commit()
    return _salida(registro)


def _salida(registro):
    return {
        'id': registro.id, 'producto_id': registro.producto_id,
        'producto_nombre': registro.producto_nombre, 'receta_id': registro.receta_id,
        'receta_version': registro.receta_version, 'ancho_cm': float(registro.ancho_cm),
        'alto_cm': float(registro.alto_cm), 'referencia': registro.referencia,
        'opciones': registro.opciones, 'resultado': registro.resultado,
        'usuario': registro.usuario_nombre, 'creado_en': registro.creado_en.isoformat() + 'Z',
    }


def presupuestos_recientes():
    return [_salida(r) for r in SavedQuoteRepository().recent()]
