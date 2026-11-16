"""Normalización explícita de telas y apertura faltante de etiquetas."""
import re
from decimal import Decimal

from sqlalchemy import func

from exceptions import ConflictError, ValidationFailed
from models import InventoryMovement, Supply, SupplyCategory, SupplyPriceHistory
from repositories.inventory import InventoryRepository
from services.production_costs import ETIQUETA_SKU

_ANCHO = re.compile(r'\bancho\s*[:=]?\s*(\d+(?:[.,]\d+)?)\s*(cm|cent[ií]metros?|m(?:ts?|etros?)?)?\b', re.I)
_REFERENCIA_ETIQUETA = 'Apertura faltante de etiqueta'


def ancho_del_nombre(nombre):
    matches = list(_ANCHO.finditer(nombre))
    if len(matches) != 1:
        raise ValidationFailed(f"No se pudo determinar un único ancho en: {nombre}")
    numero, unidad = matches[0].groups()
    valor = Decimal(numero.replace(',', '.'))
    if unidad and unidad.lower().startswith('c'):
        ancho = valor
    elif unidad or (('.' in numero or ',' in numero) and valor <= 10):
        ancho = valor * 100
    elif valor >= 100:
        ancho = valor
    else:
        raise ValidationFailed(f"Unidad de ancho ambigua en: {nombre}")
    if ancho <= 0 or ancho > 99999999 or ancho != ancho.quantize(Decimal('.01')):
        raise ValidationFailed(f"Ancho inválido en: {nombre}")
    return ancho


def normalizar_inicial(aplicar=False, commit=True):
    repo = InventoryRepository()
    ids = [row[0] for row in repo.session.query(Supply.id).join(SupplyCategory).filter(
        func.lower(SupplyCategory.name) == 'telas').order_by(Supply.id).all()]
    etiqueta_id = repo.session.query(Supply.id).filter_by(codigo_sku=ETIQUETA_SKU).scalar()
    if not ids or etiqueta_id is None:
        raise ValidationFailed("Faltan telas de categoría Telas o la etiqueta obligatoria")
    locked = {s.id: s for s in Supply.query.filter(Supply.id.in_(ids + [etiqueta_id]))
              .order_by(Supply.id).populate_existing().with_for_update().all()}
    plan = []
    for insumo_id in ids:
        tela = locked[insumo_id]
        ancho = ancho_del_nombre(tela.name)
        if tela.ancho_cm and Decimal(tela.ancho_cm) != ancho:
            raise ConflictError(f"Tela {tela.id}: el ancho existente difiere del nombre")
        if tela.es_tela and tela.unidad_medida == 'metro':
            if Decimal(tela.ancho_cm or 0) != ancho:
                raise ConflictError(f"Tela {tela.id}: tela configurada con ancho diferente")
            plan.append(f"Tela {tela.id}: ya normalizada")
            continue
        if tela.unidad_medida != 'cm' or tela.es_tela:
            raise ConflictError(f"Tela {tela.id}: unidad o clasificación incompatible; revisar manualmente")
        if tela.stock_actual is None or tela.precio_costo_unitario is None:
            raise ConflictError(f"Tela {tela.id}: falta stock o precio")
        movimientos = InventoryMovement.query.filter_by(id_insumo=tela.id).order_by(InventoryMovement.id).all()
        precios = SupplyPriceHistory.query.filter_by(id_insumo=tela.id).order_by(SupplyPriceHistory.id).all()
        if any(m.unidad not in (None, 'cm') for m in movimientos) or any(p.unidad not in (None, 'cm') for p in precios):
            raise ConflictError(f"Tela {tela.id}: historial con unidades incompatibles")
        stock = Decimal(tela.stock_actual) / 100
        minimo = Decimal(tela.stock_minimo or 0) / 100
        precio = Decimal(tela.precio_costo_unitario) * 100
        if (stock != stock.quantize(Decimal('.0001')) or minimo != minimo.quantize(Decimal('.0001'))
                or precio >= Decimal('100000000')):
            raise ValidationFailed(f"Tela {tela.id}: conversión excede la precisión admitida")
        plan.append(f"Tela {tela.id}: ancho {ancho} cm; stock {tela.stock_actual} cm -> {stock} m; "
                    f"mínimo {tela.stock_minimo or 0} cm -> {minimo} m; "
                    f"precio {tela.precio_costo_unitario}/cm -> {precio}/m")
        if aplicar:
            for m in movimientos:
                m.unidad = 'cm'
            for p in precios:
                p.unidad = 'cm'
            viejo_stock = tela.stock_actual
            tela.stock_actual, tela.stock_minimo = stock, minimo
            tela.precio_costo_unitario, tela.ancho_cm = precio, ancho
            tela.unidad_medida, tela.es_tela = 'metro', True
            repo.agregar_movimiento(InventoryMovement(
                id_insumo=tela.id, tipo='ajuste', cantidad=0, stock_resultante=stock, unidad='metro',
                referencia='Conversión de unidad de tela',
                notas=f"Conversión de stock {viejo_stock} cm a {stock} m; el historial anterior conserva unidad cm."))
            repo.agregar_precio(SupplyPriceHistory(
                id_insumo=tela.id, precio=precio, unidad='metro', precio_m2=None,
                motivo='Conversión de precio por cm a precio por metro'))
    etiqueta = locked[etiqueta_id]
    movimientos = InventoryMovement.query.filter_by(id_insumo=etiqueta_id).order_by(InventoryMovement.id).all()
    if any(m.referencia == _REFERENCIA_ETIQUETA for m in movimientos):
        plan.append("Etiqueta: apertura ya registrada")
    else:
        total = sum((Decimal(m.cantidad) for m in movimientos), Decimal(0))
        if (etiqueta.unidad_medida != 'unidad' or Decimal(etiqueta.stock_actual or 0) != 100
                or total != 0 or any(m.cantidad != 0 or m.unidad not in (None, 'unidad') for m in movimientos)):
            raise ConflictError("Etiqueta: el saldo o los movimientos cambiaron; revisar manualmente")
        plan.append("Etiqueta: registrar apertura faltante de 100 unidades sin modificar el saldo")
        if aplicar:
            repo.agregar_movimiento(InventoryMovement(
                id_insumo=etiqueta_id, tipo='apertura', cantidad=100, stock_resultante=100, unidad='unidad',
                referencia=_REFERENCIA_ETIQUETA,
                notas='Regularización del saldo existente; no se ingresaron unidades adicionales.'))
    if aplicar and commit:
        repo.commit()
    return plan
