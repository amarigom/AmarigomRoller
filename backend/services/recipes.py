from datetime import date, datetime, time
from decimal import Decimal
from types import SimpleNamespace

from flask import current_app

from exceptions import ConflictError, NotFoundError, ValidationFailed
from models import PiezaStock, Product, Receta, RecetaItem
from repositories.recipe import PieceRepository, RecipeRepository, ScrapRepository, ahora
from repositories.supply import SupplyRepository
from schemas.recipes import (
    ExplosionItemOut, ExplosionOut, ProduccionOut, ProductIn, ProductRecipeOut, RecipeItemFullOut, RecipeItemIn,
    RecipeItemOut, RecipeVersionIn, RecipeVersionOut, StockDescontadoOut,
)
from services import recipe_import
from services.costeo import calcular_explosion
from strategies import formulas
from strategies.costing import MIN_RETAZO_PERFIL_CM, STRATEGIES, usa_perfiles
from strategies.units import PieceUnit, get_unit_strategy

_CONTEXTO_PRUEBA = {'ancho': 100.0, 'alto': 100.0}


class RecipeService:
    def __init__(self, recipes=None, scraps=None, supplies=None, pieces=None):
        self.recipes = recipes or RecipeRepository()
        self.scraps = scraps or ScrapRepository()
        self.supplies = supplies or SupplyRepository()
        self.pieces = pieces or PieceRepository()

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

    def _calcular(self, product_id, w, h, opciones=None, fecha=None, version=None):
        receta = self._receta(product_id, fecha, version)
        resultado, total = self._calcular_items(receta.items, w, h, opciones)
        return receta, resultado, total

    def _calcular_items(self, componentes, w, h, opciones=None):
        ids_insumo = {c.id_insumo for c in componentes if c.id_insumo}
        ids_perfil = {c.id_insumo for c in componentes if c.id_insumo and usa_perfiles(c.tipo_calculo)}
        retazos = self.scraps.available_by_supply(ids_insumo)
        sobrantes = self.pieces.remnants_by_supply(ids_perfil)
        return calcular_explosion(
            componentes, retazos, w, h, sobrantes_perfil=sobrantes, opciones=opciones,
            min_retazo_cm=current_app.config.get('MIN_RETAZO_PERFIL_CM', MIN_RETAZO_PERFIL_CM),
        )

    @staticmethod
    def _mano_obra(resultado):
        minutos = round(sum(r['minutos'] for r in resultado), 2)
        costo_minuto = float(current_app.config.get('COSTO_MINUTO_MANO_OBRA', 0) or 0)
        return minutos, round(minutos * costo_minuto, 2)

    def explode(self, product_id, w, h, opciones=None, fecha=None, version=None):
        receta, resultado, total = self._calcular(product_id, w, h, opciones, fecha, version)
        return self._explosion_out(receta.version, resultado, total)

    def _explosion_out(self, version, resultado, total):
        minutos, mano_obra = self._mano_obra(resultado)
        return ExplosionOut(
            version=version,
            explosion=[ExplosionItemOut(**r) for r in resultado],
            total_materiales=total,
            total_minutos=minutos,
            total_mano_obra=mano_obra,
            total=round(total + mano_obra, 2),
        )

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
        resultado, total = self._calcular_items(componentes, datos.w, datos.h, datos.opciones)
        return self._explosion_out(None, resultado, total)

    def _items_transitorios(self, items):
        insumos = {s.id: s for s in self.supplies.get_many({i.id_insumo for i in items if i.id_insumo})}
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
        producto = self.create_product(ProductIn(nombre=datos.nombre, categoria=origen.producto.categoria))
        items = [RecipeItemIn(**{k: getattr(i, k) for k in RecipeItemIn.model_fields}) for i in origen.items]
        version = self.publish_version(
            producto.id, RecipeVersionIn(items=items, nota=f"Copia de {origen.producto.nombre} v{origen.version}"))
        return producto, version

    # --- Versionado ------------------------------------------------------------------------

    def publish_version(self, product_id, datos, commit=True):
        """Crea una versión nueva y cierra la vigente: los cálculos con fecha anterior no cambian."""
        if self.recipes.session.get(Product, product_id) is None:
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
        insumos = {s.id: s for s in self.supplies.get_many(ids)}
        for n, item in enumerate(items, start=1):
            pref = f"Ítem {n} ({item.nombre})"
            if item.tipo_calculo not in STRATEGIES:
                errores.append(f"{pref}: tipo de cálculo '{item.tipo_calculo}' inexistente (válidos: {', '.join(sorted(STRATEGIES))})")
                continue
            if item.tipo_calculo != 'mano_obra' and not item.id_insumo:
                errores.append(f"{pref}: falta el insumo")
            insumo = insumos.get(item.id_insumo) if item.id_insumo else None
            if item.id_insumo and insumo is None:
                errores.append(f"{pref}: el insumo {item.id_insumo} no existe")
            if insumo is not None:
                if item.tipo_calculo == 'perfil' and not insumo.largo_pieza_cm:
                    errores.append(f"{pref}: el insumo '{insumo.name}' no tiene largo de pieza cargado")
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

    def produce(self, product_id, w, h, opciones=None):
        """Confirma una producción: descuenta stock y marca como usados los retazos.

        Se recalcula en el servidor (el cliente solo manda las medidas) y todo se aplica
        en una única transacción: si algo falta, no se descuenta nada.
        """
        receta, resultado, total = self._calcular(product_id, w, h, opciones)

        retazos_ids = {r['id_retazo'] for r in resultado if r['id_retazo'] is not None}
        retazos = self.scraps.lock_available(retazos_ids)
        if retazos_ids - set(retazos):
            self.scraps.session.rollback()
            raise ConflictError("Un retazo ya fue usado por otra producción. Recalculá la receta.")

        cortes = [c for r in resultado for c in r['cortes']]
        piezas_ids = {c['id_pieza'] for c in cortes if c['id_pieza'] is not None}
        piezas = self.pieces.lock_remnants(piezas_ids)
        if piezas_ids - set(piezas):
            self.pieces.session.rollback()
            raise ConflictError("Un sobrante de perfil ya fue usado por otra producción. Recalculá la receta.")

        necesario = {}
        for r in resultado:
            if r['metodo'] not in ('RETAZO', 'MANO_OBRA') and r['id_insumo']:
                necesario[r['id_insumo']] = necesario.get(r['id_insumo'], Decimal(0)) + Decimal(str(r['consumo_m_o_m2']))

        insumos = self.supplies.lock_many(list(necesario))
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

        descontados = []
        for insumo_id, cantidad in necesario.items():
            insumo = insumos[insumo_id]
            insumo.stock_actual = Decimal(insumo.stock_actual or 0) - cantidad
            descontados.append(StockDescontadoOut(
                id_insumo=insumo_id, insumo=insumo.name, cantidad=float(cantidad),
                stock_restante=float(insumo.stock_actual), unidad=insumo.unidad_medida))
        for retazo in retazos.values():
            retazo.estado = 'usado'
        generados = self._aplicar_cortes_perfil(resultado, piezas)
        self.supplies.commit()

        minutos, mano_obra = self._mano_obra(resultado)
        return ProduccionOut(
            version=receta.version,
            descontado=descontados,
            retazos_usados=sorted(retazos),
            retazos_perfil_generados=generados,
            total_materiales=total,
            total_minutos=minutos,
            total_mano_obra=mano_obra,
            total=round(total + mano_obra, 2),
        )

    def _aplicar_cortes_perfil(self, resultado, piezas):
        """Reproduce los cortes en orden: actualiza los sobrantes usados y guarda los nuevos."""
        por_token = {}
        generados = 0
        for r in resultado:
            for corte in r['cortes']:
                origen = None
                if corte['origen'] == 'retazo':
                    origen = piezas.get(corte['id_pieza']) or por_token.get(corte['tok_origen'])
                if corte['reutilizable']:
                    if origen is not None:
                        origen.longitud_actual_cm = Decimal(str(corte['sobrante']))
                        por_token[corte['tok_sobrante']] = origen
                    else:
                        nueva = PiezaStock(
                            id_insumo=r['id_insumo'],
                            longitud_original_cm=Decimal(str(corte['largo_origen'])),
                            longitud_actual_cm=Decimal(str(corte['sobrante'])),
                            es_retazo=True,
                        )
                        self.pieces.session.add(nueva)
                        por_token[corte['tok_sobrante']] = nueva
                        generados += 1
                elif origen is not None:
                    origen.longitud_actual_cm = Decimal(0)
        return generados
