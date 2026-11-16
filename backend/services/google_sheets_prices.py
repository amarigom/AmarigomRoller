import json
from datetime import timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from urllib.parse import quote

import requests
from flask import current_app, g
from google.auth.exceptions import GoogleAuthError
from google.auth.transport.requests import Request
from google.oauth2 import service_account

from exceptions import AppError, ExternalServiceError, ValidationFailed
from models import SupplyPriceHistory
from repositories.inventory import InventoryRepository
from repositories.price_sync import PriceSyncRepository
from repositories.supply import SupplyRepository
from utils.clock import utcnow

SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'
HEADERS = ('articulo', 'descripción', 'unidad medida', 'precio final')


def _unidad(texto):
    return str(texto or '').strip().lower().replace(' ', '').replace('.', '')


def _estado(lock=False):
    estado = PriceSyncRepository().state(lock=lock)
    if estado is None:
        raise ValidationFailed('Falta el estado de sincronización; aplicá las migraciones')
    return estado


def estado_sincronizacion():
    estado = _estado()
    configurado = bool(current_app.config.get('GOOGLE_SHEETS_ID') and
                       (current_app.config.get('GOOGLE_SHEETS_CREDENTIALS_JSON') or
                        current_app.config.get('GOOGLE_APPLICATION_CREDENTIALS')))
    atrasada = not estado.ultima_exitosa or utcnow() - estado.ultima_exitosa > timedelta(hours=18)
    return {
        'configurado': configurado,
        'ultimo_intento': estado.ultimo_intento.isoformat() + 'Z' if estado.ultimo_intento else None,
        'ultima_exitosa': estado.ultima_exitosa.isoformat() + 'Z' if estado.ultima_exitosa else None,
        'error': estado.error,
        'actualizados': estado.actualizados,
        'omitidos': estado.omitidos,
        'advertencia': (not configurado or atrasada or bool(estado.error)),
    }


def _leer_hoja():
    sheet_id = current_app.config.get('GOOGLE_SHEETS_ID')
    credentials_json = current_app.config.get('GOOGLE_SHEETS_CREDENTIALS_JSON')
    credentials_file = current_app.config.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not sheet_id or not (credentials_json or credentials_file):
        raise ValidationFailed('Configurá el ID de la hoja y las credenciales de Google Sheets')
    try:
        if credentials_json:
            info = json.loads(credentials_json)
            if not isinstance(info, dict):
                raise ValueError('La credencial debe ser un objeto JSON')
            credentials = service_account.Credentials.from_service_account_info(info, scopes=[SCOPE])
        else:
            credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=[SCOPE])
        credentials.refresh(Request())
        nombre = current_app.config['GOOGLE_SHEETS_TAB'].replace("'", "''")
        rango = quote(f"'{nombre}'!A:D", safe='')
        url = f'https://sheets.googleapis.com/v4/spreadsheets/{quote(sheet_id, safe="")}/values/{rango}'
        response = requests.get(url, headers={'Authorization': f'Bearer {credentials.token}'},
                                params={'valueRenderOption': 'UNFORMATTED_VALUE'}, timeout=20)
        response.raise_for_status()
        data = response.json()
    except (OSError, ValueError, GoogleAuthError, requests.RequestException) as exc:
        current_app.logger.warning('No se pudo leer Google Sheets: %s', type(exc).__name__)
        raise ExternalServiceError('No se pudo leer la hoja; revisá el acceso y la configuración') from exc
    filas = data.get('values') if isinstance(data, dict) else None
    if not isinstance(filas, list) or len(filas) > 10000 or any(not isinstance(fila, list) for fila in filas):
        raise ValidationFailed('La hoja está vacía o supera 10.000 filas')
    return filas


def _precio_por_unidad(insumo, unidad_hoja, valor):
    try:
        precio = Decimal(str(valor))
    except (InvalidOperation, ValueError):
        raise ValidationFailed(f'{insumo.codigo_sku}: precio inválido') from None
    if not precio.is_finite() or precio <= 0:
        raise ValidationFailed(f'{insumo.codigo_sku}: el precio debe ser mayor a cero')
    if precio.adjusted() > 20 or precio.adjusted() < -20:
        raise ValidationFailed(f'{insumo.codigo_sku}: precio fuera del rango admitido')
    unidad = _unidad(unidad_hoja)
    if insumo.unidad_compra and _unidad(insumo.unidad_compra) == unidad:
        factor = Decimal(insumo.factor_conversion) if insumo.factor_conversion is not None else None
    elif unidad in ('mtlineal', 'metrolineal', 'metro', 'metros', 'mt', 'm'):
        factor = {'metro': Decimal(1), 'cm': Decimal(100)}.get(insumo.unidad_medida)
    elif unidad in ('unidad', 'unidades', 'un'):
        if insumo.unidad_medida == 'unidad':
            factor = Decimal(1)
        elif insumo.unidad_medida in ('cm', 'metro') and insumo.largo_pieza_cm:
            factor = Decimal(insumo.largo_pieza_cm)
            if insumo.unidad_medida == 'metro':
                factor /= 100
        else:
            factor = None
    elif unidad in ('rollo', 'rollos') and insumo.unidad_medida == 'rollo':
        factor = Decimal(1)
    else:
        factor = None
    if factor is None or factor <= 0:
        raise ValidationFailed(f'{insumo.codigo_sku}: unidad de compra incompatible o largo de pieza faltante')
    resultado = precio / factor
    if resultado >= Decimal('100000000'):
        raise ValidationFailed(f'{insumo.codigo_sku}: precio fuera del rango admitido')
    resultado = resultado.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    if resultado <= 0:
        raise ValidationFailed(f'{insumo.codigo_sku}: precio fuera del rango admitido')
    return resultado


def _preparar(filas):
    encabezado = None
    for indice, fila in enumerate(filas):
        if [str(v).strip().lower() for v in fila[:4]] == list(HEADERS):
            encabezado = indice
            break
    if encabezado is None:
        raise ValidationFailed('No se encontró el encabezado Articulo, Descripción, Unidad Medida, Precio Final')
    filas_datos = filas[encabezado + 1:]
    codigos = {str(f[0]).strip() for f in filas_datos if f and str(f[0]).strip()}
    existentes = SupplyRepository().active_by_skus(codigos)
    por_codigo = {s.codigo_sku: s for s in existentes}
    ids = [s.id for s in existentes]
    bloqueados = SupplyRepository().lock_many(ids)
    cambios, vistos, omitidos = {}, {}, 0
    for numero, fila in enumerate(filas_datos, encabezado + 2):
        if not fila or not str(fila[0]).strip():
            continue
        codigo = str(fila[0]).strip()
        insumo = por_codigo.get(codigo)
        if not insumo:
            omitidos += 1
            continue
        if insumo.id not in bloqueados or len(fila) < 4:
            raise ValidationFailed(f'Fila {numero}: insumo inactivo o datos incompletos: {codigo}')
        if codigo in vistos:
            if fila[:4] != vistos[codigo]:
                raise ValidationFailed(f'Fila {numero}: SKU repetido con datos diferentes: {codigo}')
            continue
        vistos[codigo] = fila[:4]
        insumo = bloqueados[insumo.id]
        cambios[insumo.id] = (insumo, _precio_por_unidad(insumo, fila[2], fila[3]))
    if not cambios:
        raise ValidationFailed('No hay artículos de la hoja que coincidan con SKU activos')
    return cambios, omitidos


def sincronizar_precios():
    repo = PriceSyncRepository()
    inventory = InventoryRepository()
    estado = _estado(lock=True)
    inicio = utcnow()
    try:
        cambios, omitidos = _preparar(_leer_hoja())
        momento = utcnow()
        usuario = getattr(g, 'current_user', None)
        actualizados = 0
        for insumo, precio in cambios.values():
            if Decimal(insumo.precio_costo_unitario or 0) == precio:
                continue
            insumo.precio_costo_unitario = precio
            inventory.agregar_precio(SupplyPriceHistory(
                id_insumo=insumo.id, precio=precio, precio_m2=insumo.precio_m2,
                unidad=insumo.unidad_medida, vigente_desde=momento,
                motivo='Sincronización Google Sheets', usuario_id=usuario.id if usuario else None,
            ))
            actualizados += 1
        estado.ultimo_intento = momento
        estado.ultima_exitosa = momento
        estado.error = None
        estado.actualizados = actualizados
        estado.omitidos = omitidos
        repo.commit()
        return {'actualizados': actualizados, 'omitidos': omitidos}
    except AppError as exc:
        repo.session.rollback()
        estado = _estado(lock=True)
        if estado.ultimo_intento is None or estado.ultimo_intento <= inicio:
            estado.ultimo_intento = utcnow()
            estado.error = exc.message
        repo.commit()
        raise
