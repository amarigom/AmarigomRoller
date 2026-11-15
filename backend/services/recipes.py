from datetime import date, datetime, time
from decimal import Decimal, ROUND_HALF_UP
from types import SimpleNamespace

from flask import current_app, g

from exceptions import ConflictError, NotFoundError, ValidationFailed
from models import InventoryMovement, PiezaStock, ProductionRecord, Product, Receta, RecetaItem, RetazoTela
from repositories.inventory import InventoryRepository
from repositories.recipe import PieceRepository, RecipeRepository, ScrapRepository, ahora
from repositories.supply import SupplyRepository
from schemas.recipes import (
    CotizacionOut, ExplosionItemOut, ExplosionOut, ProductionHistoryOut, ProduccionOut, ProductIn, ProductRecipeOut,
    RecipeItemFullOut, RecipeItemIn, RecipeItemOut, RecipeVersionIn, RecipeVersionOut, StockDescontadoOut,
)
from services import recipe_import
from services.costeo import calcular_explosion
from services.pricing import calcular_cotizacion
from services.production_costs import ETIQUETA_SKU
from strategies import formulas
from strategies.costing import MIN_RETAZO_PERFIL_CM, STRATEGIES, usa_perfiles
from strategies.units import PieceUnit, get_unit_strategy

_CONTEXTO_PRUEBA = {'ancho': 100.0, 'alto': 100.0}


class RecipeService:
    def __init__(self, recipes=None, scraps=None, supplies=None, pieces=None, inventory=None):
        self.recipes = recipes or RecipeRepository()
        self.scraps = scraps or ScrapRepository()
        self.supplies = supplies or SupplyRepository()
        self.pieces = pieces or PieceRepository()
        self.inventory = inventory or InventoryRepository()

    # --- Lectura ---------------------------------------------------------------------------

    def _receta(self, product_id, fecha=None, version=None):
        if version:
            receta = self.recipes.por_version(product_id, version)
        else:
            momento = datetime.combine(fecha, time(23, 59, 59)) if isinstance(fecha, date) else None
            receta = self.recipes.vigente(product_id, momento)
        if receta is None or not receta.items:
            raise NotFoundError(f"El producto {product_id} no tiene una receta definida para esa fecha o versión.")
        return receta

    def base_recipe(self, product_id):
        return [RecipeItemOut.from_model(c) for c in self._receta(product_id).items]

    def versions(self, product_id):
        return [RecipeVersionOut.from_model(r) for r in self.recipes.versiones(product_id)]

    @staticmethod
    def calculation_types():
        return [
            {'tipo': tipo, 'descripcion': ((type(s).__doc__ or '').strip().splitlines() or [''])[0]}
            for tipo, s in sorted(STRATEGIES.items())
        ]

    def production_history(self, product_id=None, referencia=None, limit=100, offset=0):
        if product_id is not None and self.recipes.session.get(Product, product_id) is None:
            raise NotFoundError(f"El producto {product_id} no existe")
        rows = self.recipes.historial_producciones(product_id, referencia, limit, offset)
        return [ProductionHistoryOut.from_model(r) for r in rows]

    def _calcular(self, product_id, w, h, opciones=None, fecha=None, version=None, referencia=None):
        receta = self._receta(product_id, fecha, version)
        resultado, total = self._calcular_items(receta.items, w, h, opciones, referencia)
        return receta, resultado, total

    def _calcular_items(self, componentes, w, h, opciones=None, referencia=None):
        etiqueta = self.supplies.by_sku(ETIQUETA_SKU)
        if etiqueta is None or not etiqueta.activo:
            raise ValidationFailed("Falta el insumo obligatorio Etiqueta; aplicá las migraciones o reactivá el insumo")
        if any(c.id_insumo == etiqueta.id for c in componentes):
            raise ValidationFailed("La etiqueta se agrega automáticamente; quitála de los componentes de la receta")
        etiqueta_item = SimpleNamespace(
            id_insumo=etiqueta.id, insumo=etiqueta, nombre=etiqueta.name, tipo_calculo='fijo',
            delta_ancho_cm=0, delta_alto_cm=0, cantidad_base=1, merma_pct=0, minutos_mano_obra=0,
            insumos_alternativos=[],
        )
        componentes = list(componentes) + [etiqueta_item]
        ids_insumo = {c.id_insumo for c in componentes if c.id_insumo}
        ids_perfil = {c.id_insumo for c in componentes if c.id_insumo and usa_perfiles(c.tipo_calculo)}
        ids_alt = {
            i for c in componentes if usa_perfiles(c.tipo_calculo) for i in (c.insumos_alternativos or [])
        }
        alternativos = {s.id: s for s in self.supplies.get_many(ids_alt)} if ids_alt else {}
        retazos = self.scraps.available_by_supply(ids_insumo, referencia)
        sobrantes = self.pieces.remnants_by_supply(ids_perfil | ids_alt)
        return calcular_explosion(
            componentes, retazos, w, h, sobrantes_perfil=sobrantes, opciones=opciones,
            insumos_alternativos=alternativos,
            min_retazo_cm=current_app.config.get('MIN_RETAZO_PERFIL_CM', MIN_RETAZO_PERFIL_CM),
        )

    @staticmethod
    def _mano_obra(resultado):
        minutos = round(sum(r['minutos'] for r in resultado), 2)
        costo_minuto = float(current_app.config.get('COSTO_MINUTO_MANO_OBRA', 0) or 0)
        return minutos, round(minutos * costo_minuto, 2)

    def explode(self, product_id, w, h, opciones=None, fecha=None, version=None, referencia=None):
        receta, resultado, total = self._calcular(product_id, w, h, opciones, fecha, version, referencia)
        return self._explosion_out(receta.version, resultado, total)

    def quote(self, receta, w, h, km_obra, opciones=None, referencia=None):
        resultado, total = self._calcular_items(receta.items, w, h, opciones, referencia)
        explosion = self._explosion_out(receta.version, resultado, total)
        return CotizacionOut(**explosion.model_dump(), receta_id=receta.id,
                             **calcular_cotizacion(explosion, km_obra))

    def quote_by_id(self, recipe_id, w, h, km_obra, opciones=None, referencia=None):
        receta = self.recipes.por_id(recipe_id)
        if receta is None or not receta.items:
            raise NotFoundError(f"La receta {recipe_id} no existe o no tiene componentes")
        return self.quote(receta, w, h, km_obra, opciones, referencia)

    def quote_product(self, product_id, w, h, km_obra, opciones=None, fecha=None, version=None, referencia=None):
        receta = self._receta(product_id, fecha, version)
        return self.quote(receta, w, h, km_obra, opciones, referencia)

    def _explosion_out(self, version, resultado, total):
        minutos, mano_obra = self._mano_obra(resultado)
        desgaste = self._desgaste()
        return ExplosionOut(
            version=version,
            explosion=[ExplosionItemOut(**r) for r in resultado],
            total_materiales=total,
            total_minutos=minutos,
            total_mano_obra=mano_obra,
            total_desgaste=desgaste,
            total=round(total + mano_obra + desgaste, 2),
        )

    @staticmethod
    def _desgaste():
        desgaste = Decimal(str(current_app.config['COSTO_DESGASTE_MAQUINARIA']))
        if not desgaste.is_finite() or desgaste < 0:
            raise ValueError("El costo por desgaste debe ser finito y no negativo")
        return float(desgaste.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

    # --- Herramientas de edición -----------------------------------------------------------

    def products(self):
        """Productos con la versión de receta vigente (para el panel de recetas)."""
        vigentes = {}
        for r in self.recipes.vigentes():
            vigentes.setdefault(r.producto_id, r)
        return [
            ProductRecipeOut(
                id=p.id, nombre=p.nombre, categoria=p.categoria,
                version_vigente=vigentes[p.id].version if p.id in vigentes else None,
                items=len(vigentes[p.id].items) if p.id in vigentes else 0,
            )
            for p in self.recipes.productos()
        ]

    def create_product(self, datos):
        if self.recipes.producto_por_nombre(datos.nombre) is not None:
            raise ConflictError(f"Ya existe un producto llamado '{datos.nombre}'")
        producto = Product(nombre=datos.nombre.strip(), categoria=datos.categoria, activo=True)
        self.recipes.session.add(producto)
        self.recipes.commit()
        return ProductRecipeOut(id=producto.id, nombre=producto.nombre, categoria=producto.categoria,
                                version_vigente=None, items=0)

    def version_detail(self, product_id, version=None):
        receta = self.recipes.por_version(product_id, version) if version else self.recipes.vigente(product_id)
        if receta is None:
            raise NotFoundError("Esa versión de la receta no existe")
        return [RecipeItemFullOut.from_model(i) for i in receta.items]

    def preview(self, datos):
        """Calcula una receta sin guardarla (no toca la base): vista previa para medidas de prueba."""
        self._validar_items(datos.items)
        componentes = self._items_transitorios(datos.items)
        resultado, total = self._calcular_items(
            componentes, datos.w, datos.h, datos.opciones, datos.referencia)
        return self._explosion_out(None, resultado, total)

    def _items_transitorios(self, items):
        ids = {i.id_insumo for i in items if i.id_insumo}
        insumos = {s.id: s for s in self.supplies.get_many(ids)}
        # Objetos simples: así no se agregan a la sesión de la base
        return [
            SimpleNamespace(insumo=insumos.get(i.id_insumo), **i.model_dump())
            for i in items
        ]

    def duplicate(self, product_id, datos):
        """Copia una versión de receta a un producto nuevo para armar variantes rápido."""
        origen = self.recipes.por_version(product_id, datos.version) if datos.version else self.recipes.vigente(product_id)
        if origen is None:
            raise NotFoundError("No hay una receta para duplicar")
        items = [RecipeItemIn(**{k: getattr(i, k) for k in RecipeItemIn.model_fields}) for i in origen.items]
        self._validar_items(items)
        if self.recipes.producto_por_nombre(datos.nombre) is not None:
            raise ConflictError(f"Ya existe un producto llamado '{datos.nombre}'")
        producto = Product(nombre=datos.nombre.strip(), categoria=origen.producto.categoria, activo=True)
        self.recipes.session.add(producto)
        self.recipes.session.flush()
        version = self.publish_version(
            producto.id, RecipeVersionIn(items=items, nota=f"Copia de {origen.producto.nombre} v{origen.version}"),
            commit=False)
        self.recipes.commit()
        return ProductRecipeOut(id=producto.id, nombre=producto.nombre, categoria=producto.categoria,
                                version_vigente=version.version, items=len(items)), version

    # --- Versionado ------------------------------------------------------------------------

    def publish_version(self, product_id, datos, commit=True):
        """Crea una versión nueva y cierra la vigente: los cálculos con fecha anterior no cambian."""
        producto = Product.query.filter_by(id=product_id).populate_existing().with_for_update().first()
        if producto is None:
            raise NotFoundError(f"El producto {product_id} no existe")
        self._validar_items(datos.items)

        ahora_ = ahora()
        vigente = self.recipes.vigente(product_id, ahora_)
        if vigente is not None:
            vigente.vigente_hasta = ahora_
        receta = Receta(
            producto_id=product_id,
            version=self.recipes.ultima_version(product_id) + 1,
            vigente_desde=ahora_,
            nota=datos.nota,
        )
        for orden, item in enumerate(datos.items):
            receta.items.append(RecetaItem(orden=orden, nombre=item.nombre, **item.model_dump(exclude={'nombre'})))
        self.recipes.add(receta)
        if commit:
            self.recipes.commit()
        else:
            self.recipes.session.flush()
        return RecipeVersionOut.from_model(receta)

    def import_csv(self, datos):
        """Carga recetas en lote. Todo o nada: si hay un error no se guarda ningún producto."""
        productos, errores = recipe_import.parsear(datos.csv)
        for nombre, items in productos.items():
            try:
                self._validar_items(items)
            except ValidationFailed as exc:
                errores.extend(f"{nombre}: {d}" for d in exc.detalles)
        if errores:
            raise ValidationFailed("El archivo tiene errores", detalles=errores)

        resumen = []
        try:
            for nombre, items in productos.items():
                producto = self.recipes.producto_por_nombre(nombre)
                existente = producto is not None
                version = (self.recipes.ultima_version(producto.id) if existente else 0) + 1
                if datos.aplicar:
                    if not existente:
                        producto = Product(nombre=nombre, activo=True)
                        self.recipes.session.add(producto)
                        self.recipes.session.flush()
                    self.publish_version(
                        producto.id, RecipeVersionIn(items=items, nota=datos.nota or 'Importada desde CSV'), commit=False)
                resumen.append({'producto': nombre, 'existe': existente, 'items': len(items), 'version': version})
            if datos.aplicar:
                self.recipes.commit()
        except Exception:
            self.recipes.session.rollback()
            raise
        return {'aplicado': datos.aplicar, 'productos': resumen}

    def _validar_items(self, items):
        errores = []
        ids = {i.id_insumo for i in items if i.id_insumo}
        ids |= {a for i in items for a in i.insumos_alternativos}
        insumos = {s.id: s for s in self.supplies.get_many(ids)}
        for n, item in enumerate(items, start=1):
            pref = f"Ítem {n} ({item.nombre})"
            if item.tipo_calculo not in STRATEGIES:
                errores.append(f"{pref}: tipo de cálculo '{item.tipo_calculo}' inexistente (válidos: {', '.join(sorted(STRATEGIES))})")
                continue
            if item.tipo_calculo == 'superficie':
                errores.append(f"{pref}: las recetas nuevas deben calcular la tela por metro lineal (lineal_alto)")
            if item.insumos_alternativos and item.tipo_calculo != 'perfil':
                errores.append(f"{pref}: solo los componentes de tipo 'perfil' admiten perfiles alternativos")
            for alt in item.insumos_alternativos:
                alternativo = insumos.get(alt)
                if alternativo is None:
                    errores.append(f"{pref}: el perfil alternativo {alt} no existe")
                elif not alternativo.largo_pieza_cm:
                    errores.append(f"{pref}: el perfil alternativo '{alternativo.name}' no tiene largo de pieza cargado")
                elif alternativo.unidad_medida not in ('cm', 'metro'):
                    errores.append(f"{pref}: el perfil alternativo '{alternativo.name}' requiere stock en cm o metro")
            if item.tipo_calculo != 'mano_obra' and not item.id_insumo:
                errores.append(f"{pref}: falta el insumo")
            insumo = insumos.get(item.id_insumo) if item.id_insumo else None
            if item.id_insumo and insumo is None:
                errores.append(f"{pref}: el insumo {item.id_insumo} no existe")
            if insumo is not None:
                if insumo.codigo_sku == ETIQUETA_SKU:
                    errores.append(f"{pref}: la etiqueta se agrega automáticamente")
                if item.tipo_calculo == 'perfil' and not insumo.largo_pieza_cm:
                    errores.append(f"{pref}: el insumo '{insumo.name}' no tiene largo de pieza cargado")
                if item.tipo_calculo == 'perfil' and insumo.unidad_medida not in ('cm', 'metro'):
                    errores.append(f"{pref}: los perfiles deben tener stock en cm o metro")
                if insumo.es_tela and (item.tipo_calculo != 'lineal_alto' or insumo.unidad_medida != 'metro'
                                       or not insumo.ancho_cm or insumo.ancho_cm <= 0 or insumo.precio_costo_unitario is None):
                    errores.append(f"{pref}: la tela requiere cálculo lineal_alto, ancho positivo y stock y precio por metro")
                if insumo.es_tela and item.tipo_calculo == 'lineal_alto' and (
                        item.cantidad_base != 1 or item.formula_cantidad):
                    errores.append(f"{pref}: cada corte de tela requiere un ítem separado con cantidad 1")
                if isinstance(get_unit_strategy(insumo.unidad_medida), PieceUnit) and not insumo.largo_pieza_cm:
                    errores.append(f"{pref}: '{insumo.name}' se mide en {insumo.unidad_medida} y no tiene largo de pieza")
            for campo in ('formula_ancho', 'formula_alto', 'formula_cantidad', 'condicion'):
                texto = getattr(item, campo)
                if texto is not None and not texto.strip():
                    setattr(item, campo, None)
                    continue
                if texto:
                    error = self._probar_formula(texto, numerico=campo != 'condicion')
                    if error:
                        errores.append(f"{pref}, {campo}: {error}")
        if errores:
            raise ValidationFailed("La receta tiene errores", detalles=errores)

    @staticmethod
    def _probar_formula(texto, numerico):
        try:
            arbol = formulas.compilar(texto)
            if formulas.variables(arbol) <= set(_CONTEXTO_PRUEBA):
                formulas.evaluar_numero(texto, _CONTEXTO_PRUEBA) if numerico else formulas.evaluar_condicion(texto, _CONTEXTO_PRUEBA)
        except formulas.FormulaError as exc:
            return str(exc)
        return None

    # --- Producción ------------------------------------------------------------------------

    def produce(self, product_id, w, h, opciones=None, referencia=None):
        """Confirma una producción: descuenta stock y marca como usados los retazos.

        Se recalcula en el servidor (el cliente solo manda las medidas) y todo se aplica
        en una única transacción: si algo falta, no se descuenta nada.
        """
        receta, resultado, total = self._calcular(
            product_id, w, h, opciones, referencia=referencia)

        necesario = {}
        for r in resultado:
            if r['metodo'] not in ('RETAZO', 'MANO_OBRA') and r['id_insumo']:
                necesario[r['id_insumo']] = necesario.get(r['id_insumo'], Decimal(0)) + Decimal(str(r['consumo_m_o_m2']))
        insumos = self.supplies.lock_many(list(necesario))

        retazos_ids = {r['id_retazo'] for r in resultado if r['id_retazo'] is not None}
        retazos = self.scraps.lock_available(retazos_ids, referencia)
        if retazos_ids - set(retazos):
            self.scraps.session.rollback()
            raise ConflictError("Un retazo ya fue usado por otra producción. Recalculá la receta.")

        cortes = [c for r in resultado for c in r['cortes']]
        piezas_ids = {c['id_pieza'] for c in cortes if c['id_pieza'] is not None}
        piezas = self.pieces.lock_remnants(piezas_ids)
        if piezas_ids - set(piezas):
            self.pieces.session.rollback()
            raise ConflictError("Un sobrante de perfil ya fue usado por otra producción. Recalculá la receta.")

        faltantes = []
        for insumo_id, cantidad in necesario.items():
            insumo = insumos.get(insumo_id)
            disponible = Decimal(insumo.stock_actual or 0) if insumo else Decimal(0)
            if disponible < cantidad:
                nombre = insumo.name if insumo else f"insumo {insumo_id}"
                faltantes.append(f"{nombre}: necesita {cantidad}, hay {disponible}")
        if faltantes:
            self.supplies.session.rollback()
            raise ConflictError("Stock insuficiente para producir", detalles=faltantes)

        perfiles = {r['id_insumo'] for r in resultado if r['metodo'] == 'PERFIL' and r['id_insumo']}
        piezas_fisicas = self.pieces.lock_by_supply(perfiles)
        por_insumo = {insumo_id: [] for insumo_id in perfiles}
        for pieza in piezas_fisicas:
            por_insumo[pieza.id_insumo].append(pieza)
        for insumo_id, lista in por_insumo.items():
            insumo = insumos[insumo_id]
            if insumo.unidad_medida not in ('cm', 'metro'):
                raise ConflictError(f"{insumo.name}: el stock de perfiles debe estar en cm o metro")
            saldo_cm = Decimal(insumo.stock_actual or 0) * (100 if insumo.unidad_medida == 'metro' else 1)
            largo_total = sum((Decimal(p.longitud_actual_cm) for p in lista), Decimal(0))
            if saldo_cm != largo_total:
                raise ConflictError(f"{insumo.name}: el saldo no coincide con las piezas físicas; conciliá el inventario")
        for fila in resultado:
            if fila['metodo'] != 'PERFIL':
                continue
            disponibles = por_insumo[fila['id_insumo']]
            for corte in fila['cortes']:
                if corte['origen'] == 'pieza_nueva':
                    pieza = next((p for p in disponibles if not p.es_retazo and
                                  Decimal(p.longitud_actual_cm) == Decimal(str(corte['largo_origen']))), None)
                    if pieza is None:
                        raise ConflictError(f"{insumos[fila['id_insumo']].name}: no hay una pieza física disponible para el corte")
                    disponibles.remove(pieza)
                    corte['id_pieza'] = pieza.id
                    piezas[pieza.id] = pieza
                elif corte['id_pieza'] is not None:
                    pieza = piezas.get(corte['id_pieza'])
                    if pieza is None or Decimal(pieza.longitud_actual_cm) != Decimal(str(corte['largo_origen'])):
                        raise ConflictError("Un sobrante de perfil cambió; recalculá la receta")

        minutos, mano_obra = self._mano_obra(resultado)
        desgaste = self._desgaste()
        total_final = round(total + mano_obra + desgaste, 2)
        detalle = [
            {key: value for key, value in fila.items() if key != 'retazo_tela'}
            for fila in resultado
        ]
        produccion = ProductionRecord(
            producto_id=product_id,
            producto_nombre=receta.producto.nombre,
            receta_id=receta.id,
            receta_version=receta.version,
            ancho_cm=w,
            alto_cm=h,
            opciones=opciones or {},
            referencia=referencia,
            total_materiales=total,
            total_minutos=minutos,
            total_mano_obra=mano_obra,
            total_desgaste=desgaste,
            total=total_final,
            detalle=detalle,
            usuario_id=self._usuario_id(),
            usuario_nombre=getattr(getattr(g, 'current_user', None), 'nombre', None),
        )
        self.recipes.add(produccion)
        self.recipes.session.flush()

        descontados = []
        referencia_movimiento = f"Producto {product_id}, receta v{receta.version}, {w:g}x{h:g} cm"
        if referencia:
            referencia_movimiento = f"{referencia}: {referencia_movimiento}"
        for insumo_id, cantidad in necesario.items():
            insumo = insumos[insumo_id]
            insumo.stock_actual = Decimal(insumo.stock_actual or 0) - cantidad
            self.inventory.agregar_movimiento(InventoryMovement(
                id_insumo=insumo_id, tipo='consumo', cantidad=-cantidad,
                stock_resultante=insumo.stock_actual, unidad=insumo.unidad_medida, referencia=referencia_movimiento,
                notas='Consumo por producción', usuario_id=self._usuario_id(), produccion_id=produccion.id,
            ))
            descontados.append(StockDescontadoOut(
                id_insumo=insumo_id, insumo=insumo.name, cantidad=float(cantidad),
                stock_restante=float(insumo.stock_actual), unidad=insumo.unidad_medida))
        for retazo in retazos.values():
            retazo.estado = 'usado'
        generados = self._aplicar_cortes_perfil(resultado, piezas)
        retazos_tela_generados = self._aplicar_retazos_tela(resultado, referencia_movimiento)
        self.supplies.commit()

        return ProduccionOut(
            produccion_id=produccion.id,
            version=receta.version,
            descontado=descontados,
            retazos_usados=sorted(retazos),
            retazos_perfil_generados=generados,
            retazos_tela_generados=retazos_tela_generados,
            total_materiales=total,
            total_minutos=minutos,
            total_mano_obra=mano_obra,
            total_desgaste=desgaste,
            total=total_final,
        )

    @staticmethod
    def _usuario_id():
        usuario = getattr(g, 'current_user', None)
        return usuario.id if usuario else None

    def _aplicar_retazos_tela(self, resultado, referencia):
        minimo = float(current_app.config.get('MIN_RETAZO_TELA_CM', 80))
        generados = 0
        for fila in resultado:
            retazo = fila.get('retazo_tela')
            if not retazo or retazo['ancho_cm'] <= minimo or retazo['largo_cm'] <= minimo:
                continue
            self.scraps.add(RetazoTela(
                id_insumo_base=retazo['id_insumo'], ancho_cm=retazo['ancho_cm'],
                largo_cm=retazo['largo_cm'], estado='disponible',
                referencia=referencia, notas='Retazo generado automáticamente al cortar un rollo',
            ))
            generados += 1
        return generados

    def _aplicar_cortes_perfil(self, resultado, piezas):
        """Reproduce los cortes en orden: actualiza los sobrantes usados y guarda los nuevos."""
        por_token = {}
        generados = 0
        for r in resultado:
            for corte in r['cortes']:
                origen = piezas.get(corte['id_pieza']) or por_token.get(corte['tok_origen'])
                if corte['reutilizable']:
                    if origen is not None:
                        origen.longitud_actual_cm = Decimal(str(corte['sobrante']))
                        if not origen.es_retazo:
                            origen.es_retazo = True
                            generados += 1
                        por_token[corte['tok_sobrante']] = origen
                    else:
                        raise ConflictError("No se encontró la pieza física del corte; recalculá la receta")
                elif origen is not None:
                    origen.longitud_actual_cm = Decimal(0)
                else:
                    raise ConflictError("No se encontró la pieza física del corte; recalculá la receta")
        return generados
