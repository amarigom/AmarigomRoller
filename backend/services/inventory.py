from decimal import Decimal
import csv
import io
import json

from flask import g
from sqlalchemy.exc import IntegrityError

from exceptions import ConflictError, NotFoundError, ValidationFailed
from models import InventoryMovement, PiezaStock, Supply, SupplyPriceHistory
from repositories.inventory import InventoryRepository
from repositories.supply import CategoryRepository, SupplyRepository
from schemas.inventory import (
    BulkPriceIn, BulkPriceItemIn, CategoryOut, InventoryMovementIn, InventoryMovementOut, PriceHistoryOut,
    ScrapOut, StockAlertOut, SupplyOut,
)
from utils.clock import utcnow
from services.production_costs import ETIQUETA_SKU


class InventoryService:
    def __init__(self, supplies=None, categories=None, inventory=None):
        self.supplies = supplies or SupplyRepository()
        self.categories = categories or CategoryRepository()
        self.inventory = inventory or InventoryRepository()

    def list_supplies(self, limit=None, offset=0):
        supplies = self.supplies.list(limit, offset)
        perfiles, resumen = self.inventory.resumen_perfiles([s.id for s in supplies])
        return [SupplyOut.from_model(s, s.id in perfiles, resumen.get(s.id)) for s in supplies]

    def create_supply(self, datos):
        if not self.supplies.category_exists(datos.categoria_id):
            raise NotFoundError("La categoría indicada no existe")
        insumo = self.supplies.add(Supply(**datos.model_dump()))
        try:
            self.supplies.session.flush()
            self.inventory.agregar_movimiento(InventoryMovement(
                id_insumo=insumo.id, tipo='apertura', cantidad=datos.stock_actual,
                stock_resultante=datos.stock_actual, unidad=insumo.unidad_medida, referencia='Alta de insumo',
                usuario_id=self._usuario_id(),
            ))
            self.inventory.agregar_precio(SupplyPriceHistory(
                id_insumo=insumo.id, precio=datos.precio_costo_unitario,
                precio_m2=datos.precio_m2, unidad=insumo.unidad_medida,
                motivo='Precio inicial', usuario_id=self._usuario_id(),
            ))
            self.supplies.commit()
        except (ConflictError, IntegrityError) as e:
            self.supplies.session.rollback()
            raise ConflictError("El código SKU ya existe") from e
        return SupplyOut.from_model(self.supplies.get_with_category(insumo.id))

    @staticmethod
    def _usuario_id():
        usuario = getattr(g, 'current_user', None)
        return usuario.id if usuario else None

    def registrar_movimiento(self, supply_id, datos):
        insumo = self.supplies.lock_many([supply_id]).get(supply_id)
        if insumo is None:
            raise NotFoundError("Insumo no encontrado")
        if self.inventory.es_perfil(supply_id) or self.inventory.piezas_por_insumo(supply_id):
            raise ConflictError("El perfil se controla por piezas físicas; no permite movimientos de saldo genéricos")
        cantidad = Decimal(str(datos.cantidad))
        stock = Decimal(insumo.stock_actual or 0) + cantidad
        if stock < 0:
            raise ConflictError(
                "El movimiento dejaría el stock en negativo",
                detalles=[f"{insumo.name}: stock actual {insumo.stock_actual}, movimiento {cantidad}"],
            )
        insumo.stock_actual = stock
        movimiento = InventoryMovement(
            id_insumo=insumo.id, tipo=datos.tipo, cantidad=cantidad, stock_resultante=stock,
            unidad=insumo.unidad_medida, referencia=datos.referencia, notas=datos.notas, usuario_id=self._usuario_id(),
        )
        self.inventory.agregar_movimiento(movimiento)
        self.inventory.commit()
        return InventoryMovementOut.from_model(movimiento)

    def ingresar_piezas(self, supply_id, datos):
        insumo = self.supplies.lock_many([supply_id]).get(supply_id)
        if insumo is None:
            raise NotFoundError("Insumo no encontrado")
        if insumo.unidad_medida not in ('cm', 'metro') or not insumo.largo_pieza_cm:
            raise ConflictError("La pieza requiere unidad cm o metro y largo de pieza configurado")
        piezas = self.inventory.piezas_por_insumo(supply_id)
        factor = Decimal(100) if insumo.unidad_medida == 'metro' else Decimal(1)
        largo_total = sum((Decimal(p.longitud_actual_cm) for p in piezas), Decimal(0))
        if largo_total != Decimal(insumo.stock_actual or 0) * factor:
            raise ConflictError("El saldo no coincide con las piezas existentes; conciliá el inventario antes de ingresar más")
        largo = Decimal(insumo.largo_pieza_cm)
        cantidad = largo * datos.cantidad / factor
        insumo.stock_actual = Decimal(insumo.stock_actual or 0) + cantidad
        for _ in range(datos.cantidad):
            self.inventory.session.add(PiezaStock(
                id_insumo=supply_id, longitud_original_cm=largo, longitud_actual_cm=largo, es_retazo=False))
        movimiento = InventoryMovement(
            id_insumo=supply_id, tipo='entrada', cantidad=cantidad, stock_resultante=insumo.stock_actual,
            unidad=insumo.unidad_medida, referencia=datos.referencia, notas=f"Ingreso de {datos.cantidad} pieza(s) de {largo} cm",
            usuario_id=self._usuario_id())
        self.inventory.agregar_movimiento(movimiento)
        self.inventory.commit()
        return InventoryMovementOut.from_model(movimiento)

    @staticmethod
    def _pieza_dict(pieza):
        return {
            'id': pieza.id,
            'longitud_original_cm': str(pieza.longitud_original_cm),
            'longitud_actual_cm': str(pieza.longitud_actual_cm),
            'es_retazo': pieza.es_retazo,
        }

    def estado_piezas(self, supply_id):
        insumo = self.supplies.get_with_category(supply_id)
        if insumo is None:
            raise NotFoundError("Insumo no encontrado")
        piezas = self.inventory.piezas_por_insumo(supply_id)
        if not (self.inventory.es_perfil(supply_id) or piezas):
            raise ConflictError("El insumo no se controla por piezas físicas")
        movimientos = InventoryMovement.query.filter_by(id_insumo=supply_id).all()
        saldo_historial = None
        if all(m.unidad in (None, insumo.unidad_medida) for m in movimientos):
            saldo_historial = str(sum((Decimal(m.cantidad) for m in movimientos), Decimal(0)))
        return {
            'stock': str(insumo.stock_actual or 0), 'unidad': insumo.unidad_medida,
            'saldo_historial': saldo_historial, 'piezas': [self._pieza_dict(p) for p in piezas],
        }

    def conciliar_piezas(self, supply_id, datos, commit=True):
        insumo = self.supplies.lock_many([supply_id]).get(supply_id)
        if insumo is None:
            raise NotFoundError("Insumo no encontrado")
        piezas = self.inventory.piezas_por_insumo(supply_id)
        if not (self.inventory.es_perfil(supply_id) or piezas):
            raise ConflictError("El insumo no se controla por piezas físicas")
        if insumo.unidad_medida not in ('cm', 'metro') or not insumo.largo_pieza_cm:
            raise ConflictError("El perfil requiere unidad cm o metro y largo de pieza configurado")
        actuales = {p.id: p for p in piezas}
        esperadas = {p.id: p for p in datos.piezas_esperadas}
        if (Decimal(insumo.stock_actual or 0) != datos.stock_esperado
                or set(actuales) != set(esperadas)
                or any(Decimal(actuales[i].longitud_original_cm) != p.longitud_original_cm
                       or Decimal(actuales[i].longitud_actual_cm) != p.longitud_actual_cm
                       or actuales[i].es_retazo != p.es_retazo for i, p in esperadas.items())):
            raise ConflictError("El inventario cambió desde la consulta; recargá antes de conciliar")
        ids = {p.id for p in datos.piezas if p.id is not None}
        if ids != set(actuales):
            raise ValidationFailed("Incluí todas las piezas existentes; indicá longitud cero para dar de baja")
        for p in datos.piezas:
            if p.id is not None and p.longitud_original_cm != Decimal(actuales[p.id].longitud_original_cm):
                raise ValidationFailed("No se puede cambiar la longitud original de una pieza existente")
            if p.id is None and p.longitud_original_cm != Decimal(insumo.largo_pieza_cm):
                raise ValidationFailed("La longitud original debe coincidir con la barra del insumo")
        factor = Decimal(100) if insumo.unidad_medida == 'metro' else Decimal(1)
        stock = sum((p.longitud_actual_cm for p in datos.piezas), Decimal(0)) / factor
        if stock >= Decimal('100000000'):
            raise ValidationFailed("El saldo resultante excede la precisión admitida")
        movimientos = InventoryMovement.query.filter_by(id_insumo=supply_id).all()
        if any(m.unidad not in (None, insumo.unidad_medida) for m in movimientos):
            raise ConflictError("El historial contiene distintas unidades; revisalo antes de conciliar")
        saldo_anterior = Decimal(insumo.stock_actual or 0)
        diferencia_historial = saldo_anterior - sum((Decimal(m.cantidad) for m in movimientos), Decimal(0))
        if diferencia_historial:
            self.inventory.agregar_movimiento(InventoryMovement(
                id_insumo=supply_id, tipo='ajuste', cantidad=diferencia_historial,
                stock_resultante=saldo_anterior, unidad=insumo.unidad_medida,
                referencia='Regularización de historial',
                notas=f"Saldo anterior no explicado por movimientos. Motivo: {datos.motivo}",
                usuario_id=self._usuario_id()))
        antes = [self._pieza_dict(p) for p in piezas]
        for p in datos.piezas:
            pieza = actuales.get(p.id) if p.id else PiezaStock(id_insumo=supply_id)
            pieza.longitud_original_cm = p.longitud_original_cm
            pieza.longitud_actual_cm = p.longitud_actual_cm
            pieza.es_retazo = p.es_retazo
            if p.id is None:
                self.inventory.session.add(pieza)
                piezas.append(pieza)
        diferencia = stock - saldo_anterior
        insumo.stock_actual = stock
        self.inventory.session.flush()
        movimiento = InventoryMovement(
            id_insumo=supply_id, tipo='ajuste', cantidad=diferencia, stock_resultante=stock,
            unidad=insumo.unidad_medida, referencia='Conciliación de piezas',
            notas=json.dumps({'motivo': datos.motivo, 'antes': antes,
                              'despues': [self._pieza_dict(p) for p in piezas]}, ensure_ascii=False),
            usuario_id=self._usuario_id())
        self.inventory.agregar_movimiento(movimiento)
        if commit:
            self.inventory.commit()
        else:
            self.inventory.session.flush()
        return movimiento

    def ingresar_compra(self, supply_id, datos):
        insumo = self.supplies.lock_many([supply_id]).get(supply_id)
        if insumo is None:
            raise NotFoundError("Insumo no encontrado")
        if not insumo.unidad_compra or insumo.factor_conversion is None:
            raise ConflictError("Configurá la unidad de compra y el factor de conversión")
        if insumo.unidad_compra.strip().lower() in ('rollo', 'barra', 'caja') and datos.cantidad % 1:
            raise ValidationFailed("La compra de rollos, barras o cajas debe ser en unidades enteras")
        convertido = datos.cantidad * Decimal(insumo.factor_conversion)
        if convertido != convertido.quantize(Decimal('0.0001')):
            raise ValidationFailed("La compra convertida supera la precisión de cuatro decimales del stock")
        return self.registrar_movimiento(supply_id, InventoryMovementIn(
            tipo='entrada', cantidad=float(convertido), referencia=datos.referencia,
            notas=f"Compra: {datos.cantidad} {insumo.unidad_compra}; factor {insumo.factor_conversion}",
        ))

    def movimientos(self, supply_id, limit=100):
        if self.supplies.get(supply_id) is None:
            raise NotFoundError("Insumo no encontrado")
        return [InventoryMovementOut.from_model(m) for m in self.inventory.movimientos(supply_id, limit)]

    def _saldo_movimientos(self, insumo):
        total = Decimal(0)
        movimientos = InventoryMovement.query.filter_by(id_insumo=insumo.id).all()
        if (any(m.unidad is None and m.cantidad != 0 for m in movimientos)
                and any(m.unidad not in (None, insumo.unidad_medida) for m in movimientos)):
            raise ConflictError(f"{insumo.name}: el historial tiene unidades mixtas y movimientos sin unidad; revisalo manualmente")
        for movimiento in movimientos:
            unidad = movimiento.unidad or insumo.unidad_medida
            cantidad = Decimal(movimiento.cantidad)
            if unidad == insumo.unidad_medida:
                total += cantidad
            elif insumo.es_tela and unidad == 'cm' and insumo.unidad_medida == 'metro':
                total += cantidad / 100
            else:
                raise ConflictError(f"{insumo.name}: el historial contiene unidades incompatibles; revisalo manualmente")
        if total != total.quantize(Decimal('0.0001')) or abs(total) >= Decimal('10000000000'):
            raise ConflictError(f"{insumo.name}: el saldo del historial excede la precisión admitida; revisalo manualmente")
        return total

    def estado_conciliacion(self, supply_id):
        insumo = self.supplies.get_with_category(supply_id)
        if insumo is None:
            raise NotFoundError("Insumo no encontrado")
        historial = self._saldo_movimientos(insumo)
        stock = Decimal(insumo.stock_actual or 0)
        return {'stock': str(stock), 'historial': str(historial), 'unidad': insumo.unidad_medida,
                'diferencia': str(stock - historial)}

    def conciliar_stock(self, supply_id, datos):
        insumo = self.supplies.lock_many([supply_id]).get(supply_id)
        if insumo is None:
            raise NotFoundError("Insumo no encontrado")
        if self.inventory.es_perfil(supply_id) or self.inventory.piezas_por_insumo(supply_id):
            raise ConflictError("Este insumo se concilia mediante sus piezas físicas")
        saldo = Decimal(insumo.stock_actual or 0)
        historial = self._saldo_movimientos(insumo)
        if saldo != datos.stock_esperado or historial != datos.historial_esperado:
            raise ConflictError("El inventario cambió desde la consulta; recargá antes de conciliar")
        ajuste_historial = saldo - historial
        ajuste_conteo = datos.stock_contado - saldo
        if abs(ajuste_historial) >= Decimal('10000000000'):
            raise ConflictError("La regularización excede la precisión admitida; revisá el historial")
        if not ajuste_historial and not ajuste_conteo:
            raise ConflictError("El saldo, historial y conteo ya coinciden")
        if ajuste_historial:
            self.inventory.agregar_movimiento(InventoryMovement(
                id_insumo=supply_id, tipo='ajuste', cantidad=ajuste_historial, stock_resultante=saldo,
                unidad=insumo.unidad_medida, referencia='Regularización de historial',
                notas=f"Saldo anterior no explicado por movimientos. Motivo: {datos.motivo}",
                usuario_id=self._usuario_id()))
        if ajuste_conteo:
            insumo.stock_actual = datos.stock_contado
            self.inventory.agregar_movimiento(InventoryMovement(
                id_insumo=supply_id, tipo='ajuste', cantidad=ajuste_conteo, stock_resultante=datos.stock_contado,
                unidad=insumo.unidad_medida, referencia='Conciliación de stock', notas=datos.motivo,
                usuario_id=self._usuario_id()))
        self.inventory.commit()
        return {'stock': str(datos.stock_contado), 'ajuste_historial': str(ajuste_historial),
                'ajuste_conteo': str(ajuste_conteo), 'unidad': insumo.unidad_medida}

    def actualizar_stock_minimo(self, supply_id, stock_minimo):
        insumo = self.supplies.lock_many([supply_id]).get(supply_id)
        if insumo is None:
            raise NotFoundError("Insumo no encontrado")
        insumo.stock_minimo = Decimal(str(stock_minimo))
        self.supplies.commit()
        return SupplyOut.from_model(self.supplies.get_with_category(supply_id))

    def alertas_stock(self):
        return [
            StockAlertOut(
                id_insumo=s.id, insumo=s.name, stock_actual=float(s.stock_actual or 0),
                stock_minimo=float(s.stock_minimo or 0),
                faltante=max(0, float(s.stock_minimo or 0) - float(s.stock_actual or 0)),
                unidad=s.unidad_medida,
            )
            for s in self.inventory.alertas_stock()
        ]

    def retazos_disponibles(self, limit=500):
        return [ScrapOut.from_model(r) for r in self.inventory.retazos_disponibles(limit)]

    def reservar_retazo(self, scrap_id, referencia):
        retazo = self.inventory.retazo_bloqueado(scrap_id)
        if retazo is None:
            raise NotFoundError("Retazo no encontrado")
        if retazo.estado != 'disponible':
            raise ConflictError("El retazo ya no está disponible")
        retazo.estado = 'reservado'
        retazo.referencia = referencia.strip()
        self.inventory.commit()
        return ScrapOut.from_model(retazo)

    def liberar_retazo(self, scrap_id):
        retazo = self.inventory.retazo_bloqueado(scrap_id)
        if retazo is None:
            raise NotFoundError("Retazo no encontrado")
        if retazo.estado != 'reservado':
            raise ConflictError("Solo se pueden liberar retazos reservados")
        retazo.estado = 'disponible'
        retazo.referencia = None
        self.inventory.commit()
        return ScrapOut.from_model(retazo)

    def historial_precios(self, supply_id):
        if self.supplies.get(supply_id) is None:
            raise NotFoundError("Insumo no encontrado")
        return [PriceHistoryOut.from_model(p) for p in self.inventory.historial_precios(supply_id)]

    def actualizar_precios(self, datos):
        if datos.porcentaje is not None:
            supplies = self.supplies.list()
            factor = Decimal('1') + Decimal(str(datos.porcentaje)) / Decimal('100')
            cambios = {s.id: None for s in supplies}
        else:
            cambios = {i.id_insumo: Decimal(str(i.precio)) for i in datos.items or []}
        insumos = self.supplies.lock_many(cambios)
        faltantes = sorted(set(cambios) - set(insumos))
        if faltantes:
            raise NotFoundError("No existen todos los insumos de la lista", detalles=[str(i) for i in faltantes])
        momento = utcnow()
        precios_m2 = {
            i.id_insumo: Decimal(str(i.precio_m2))
            for i in datos.items or [] if i.precio_m2 is not None
        }
        if any(not insumos[supply_id].es_tela for supply_id in precios_m2):
            raise ConflictError("El precio por m² solo se puede asignar a telas")
        modificados = 0
        for supply_id, precio in cambios.items():
            insumo = insumos[supply_id]
            if datos.porcentaje is not None:
                precio = (Decimal(insumo.precio_costo_unitario or 0) * factor).quantize(Decimal('0.0001'))
            precio_m2 = precios_m2.get(supply_id, insumo.precio_m2)
            if datos.porcentaje is not None and insumo.precio_m2 is not None:
                precio_m2 = (Decimal(insumo.precio_m2) * factor).quantize(Decimal('0.0001'))
            if Decimal(insumo.precio_costo_unitario or 0) == precio and insumo.precio_m2 == precio_m2:
                continue
            insumo.precio_costo_unitario = precio
            insumo.precio_m2 = precio_m2
            modificados += 1
            self.inventory.agregar_precio(SupplyPriceHistory(
                id_insumo=supply_id, precio=precio, precio_m2=precio_m2, vigente_desde=momento,
                unidad=insumo.unidad_medida,
                motivo=datos.motivo or ('Actualización masiva' if datos.porcentaje is None else
                                        f'Ajuste masivo {datos.porcentaje:g}%'),
                usuario_id=self._usuario_id(),
            ))
        self.inventory.commit()
        return {'actualizados': modificados}

    def configurar_tela(self, supply_id, datos):
        insumo = self.supplies.lock_many([supply_id]).get(supply_id)
        if insumo is None:
            raise NotFoundError("Insumo no encontrado")
        if insumo.unidad_medida != 'metro':
            raise ConflictError("La tela debe tener stock y precio por metro lineal; no se convierten saldos automáticamente")
        insumo.es_tela = True
        insumo.ancho_cm = Decimal(str(datos.ancho_cm))
        insumo.largo_pieza_cm = Decimal(str(datos.largo_pieza_cm)) if datos.largo_pieza_cm is not None else None
        if 'precio_m2' in datos.model_fields_set:
            insumo.precio_m2 = Decimal(str(datos.precio_m2)) if datos.precio_m2 is not None else None
        insumo.unidad_compra = datos.unidad_compra
        insumo.factor_conversion = datos.factor_conversion
        self.inventory.agregar_precio(SupplyPriceHistory(
            id_insumo=insumo.id, precio=insumo.precio_costo_unitario,
            unidad=insumo.unidad_medida, precio_m2=insumo.precio_m2, motivo='Configuración de tela', usuario_id=self._usuario_id(),
        ))
        self.inventory.commit()
        return SupplyOut.from_model(self.supplies.get_with_category(insumo.id))

    def importar_precios_tela(self, datos):
        reader = csv.DictReader(io.StringIO(datos.csv.lstrip('\ufeff')), delimiter=';')
        columnas = set(reader.fieldnames or [])
        if (columnas not in ({'id_insumo', 'precio_metro'}, {'id_insumo', 'precio_metro', 'precio_m2'})
                or len(reader.fieldnames or []) != len(columnas)):
            raise ValidationFailed("El CSV debe tener las columnas id_insumo;precio_metro (precio_m2 histórico es opcional)")
        items = []
        errores = []
        for numero, fila in enumerate(reader, 2):
            if numero > 501:
                raise ValidationFailed("El CSV admite hasta 500 filas")
            if None in fila:
                errores.append(f"Fila {numero}: hay más columnas que en el encabezado")
                continue
            try:
                items.append(BulkPriceItemIn.model_validate({
                    'id_insumo': fila['id_insumo'],
                    'precio': fila['precio_metro'].replace(',', '.'),
                    'precio_m2': fila['precio_m2'].replace(',', '.') if 'precio_m2' in columnas else None,
                }))
            except (ValueError, KeyError, AttributeError) as exc:
                errores.append(f"Fila {numero}: {exc}")
        if errores:
            raise ValidationFailed("CSV de precios inválido", detalles=errores)
        if not items:
            raise ValidationFailed("El CSV no contiene precios")
        ids = [item.id_insumo for item in items]
        if len(set(ids)) != len(ids):
            raise ValidationFailed("El CSV contiene insumos repetidos")
        insumos = {s.id: s for s in self.supplies.get_many(ids)}
        invalidos = [str(i) for i in ids if i not in insumos or not insumos[i].es_tela]
        if invalidos:
            raise ValidationFailed("El CSV contiene insumos inexistentes o que no son telas", detalles=invalidos)
        if not datos.aplicar:
            return {'aplicado': False, 'filas': len(items)}
        resultado = self.actualizar_precios(BulkPriceIn(items=items, motivo=datos.motivo or 'Lista de proveedor'))
        return {'aplicado': True, 'filas': len(items), **resultado}

    def delete_supply(self, supply_id):
        insumo = self.supplies.get(supply_id)
        if insumo is None:
            raise NotFoundError("Insumo no encontrado")
        if not insumo.activo:
            raise NotFoundError("El insumo ya está archivado")
        if insumo.codigo_sku == ETIQUETA_SKU:
            raise ConflictError("La etiqueta es obligatoria para calcular y producir")
        if Decimal(insumo.stock_actual or 0) != 0:
            raise ConflictError("No se puede archivar un insumo con stock; ajustalo a cero primero")
        if self.inventory.insumo_en_receta(supply_id) or self.inventory.insumo_tiene_retazos_o_piezas(supply_id):
            raise ConflictError("No se puede archivar: el insumo se usa en recetas, retazos o stock de perfiles")
        insumo.activo = False
        self.supplies.commit()

    def list_categories(self):
        return [CategoryOut.from_model(c) for c in self.categories.list()]
