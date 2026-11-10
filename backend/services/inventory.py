from decimal import Decimal

from flask import g
from sqlalchemy.exc import IntegrityError

from exceptions import ConflictError, NotFoundError
from models import InventoryMovement, Supply, SupplyPriceHistory
from repositories.inventory import InventoryRepository
from repositories.supply import CategoryRepository, SupplyRepository
from schemas.inventory import (
    CategoryOut, InventoryMovementOut, PriceHistoryOut, ScrapOut, StockAlertOut, SupplyOut,
)
from utils.clock import utcnow


class InventoryService:
    def __init__(self, supplies=None, categories=None, inventory=None):
        self.supplies = supplies or SupplyRepository()
        self.categories = categories or CategoryRepository()
        self.inventory = inventory or InventoryRepository()

    def list_supplies(self, limit=None, offset=0):
        return [SupplyOut.from_model(s) for s in self.supplies.list(limit, offset)]

    def create_supply(self, datos):
        if not self.supplies.category_exists(datos.categoria_id):
            raise NotFoundError("La categoría indicada no existe")
        insumo = self.supplies.add(Supply(**datos.model_dump()))
        try:
            self.supplies.session.flush()
            self.inventory.agregar_movimiento(InventoryMovement(
                id_insumo=insumo.id, tipo='apertura', cantidad=datos.stock_actual,
                stock_resultante=datos.stock_actual, referencia='Alta de insumo',
                usuario_id=self._usuario_id(),
            ))
            self.inventory.agregar_precio(SupplyPriceHistory(
                id_insumo=insumo.id, precio=datos.precio_costo_unitario,
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
            referencia=datos.referencia, notas=datos.notas, usuario_id=self._usuario_id(),
        )
        self.inventory.agregar_movimiento(movimiento)
        self.inventory.commit()
        return InventoryMovementOut.from_model(movimiento)

    def movimientos(self, supply_id, limit=100):
        if self.supplies.get(supply_id) is None:
            raise NotFoundError("Insumo no encontrado")
        return [InventoryMovementOut.from_model(m) for m in self.inventory.movimientos(supply_id, limit)]

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
            cambios = {s.id: (Decimal(s.precio_costo_unitario or 0) * factor).quantize(Decimal('0.0001'))
                       for s in supplies}
        else:
            cambios = {i.id_insumo: Decimal(str(i.precio)) for i in datos.items or []}
        insumos = self.supplies.lock_many(cambios)
        faltantes = sorted(set(cambios) - set(insumos))
        if faltantes:
            raise NotFoundError("No existen todos los insumos de la lista", detalles=[str(i) for i in faltantes])
        momento = utcnow()
        modificados = 0
        for supply_id, precio in cambios.items():
            insumo = insumos[supply_id]
            if Decimal(insumo.precio_costo_unitario or 0) == precio:
                continue
            insumo.precio_costo_unitario = precio
            modificados += 1
            self.inventory.agregar_precio(SupplyPriceHistory(
                id_insumo=supply_id, precio=precio, vigente_desde=momento,
                motivo=datos.motivo or ('Actualización masiva' if datos.porcentaje is None else
                                        f'Ajuste masivo {datos.porcentaje:g}%'),
                usuario_id=self._usuario_id(),
            ))
        self.inventory.commit()
        return {'actualizados': modificados}

    def delete_supply(self, supply_id):
        insumo = self.supplies.get(supply_id)
        if insumo is None:
            raise NotFoundError("Insumo no encontrado")
        if not insumo.activo:
            raise NotFoundError("El insumo ya está archivado")
        if Decimal(insumo.stock_actual or 0) != 0:
            raise ConflictError("No se puede archivar un insumo con stock; ajustalo a cero primero")
        if self.inventory.insumo_en_receta(supply_id) or self.inventory.insumo_tiene_retazos_o_piezas(supply_id):
            raise ConflictError("No se puede archivar: el insumo se usa en recetas, retazos o stock de perfiles")
        insumo.activo = False
        self.supplies.commit()

    def list_categories(self):
        return [CategoryOut.from_model(c) for c in self.categories.list()]
