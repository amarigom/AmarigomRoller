"""Estrategias de cálculo de consumo y costo según el `tipo_calculo` de cada componente de la receta.

Para sumar un tipo nuevo basta con crear una subclase de CalculationStrategy y
registrarla en STRATEGIES (o con register_strategy).
"""
import math
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from exceptions import UnprocessableError
from strategies.units import get_unit_strategy

MIN_RETAZO_PERFIL_CM = 95.0


@dataclass
class ComponentInput:
    nombre: str
    unidad: str
    precio_unitario: float
    ancho_corte: float
    alto_corte: float
    cantidad_base: float = 1.0
    retazos: list = field(default_factory=list)
    merma_pct: float = 0.0
    minutos: float = 0.0
    largo_pieza_cm: float | None = None
    min_retazo_cm: float = MIN_RETAZO_PERFIL_CM


@dataclass
class ComponentCost:
    componente: str
    consumo_m_o_m2: float
    unidad: str
    consumo_cm: float
    medida_corte: str
    precio_unitario: float
    costo_parcial: float
    metodo: str
    id_retazo: int | None = None
    mensaje: str = ""
    merma_pct: float = 0.0
    minutos: float = 0.0
    cortes: list = field(default_factory=list)


def buscar_retazo(retazos, ancho_corte, alto_corte):
    """Devuelve el retazo disponible más chico que cubre la medida, o None."""
    candidatos = [
        r for r in retazos
        if float(r.ancho_cm) >= ancho_corte and float(r.largo_cm) >= alto_corte
    ]
    if not candidatos:
        return None
    return min(candidatos, key=lambda r: float(r.ancho_cm) * float(r.largo_cm))


class CalculationStrategy(ABC):
    tipo = ''

    @abstractmethod
    def calculate(self, data: ComponentInput) -> ComponentCost:
        ...

    @staticmethod
    def _medida(data):
        return f"{data.ancho_corte} x {data.alto_corte} cm"

    @staticmethod
    def _convertir(data, cm_lineales, ancho_cm, por_superficie):
        try:
            return get_unit_strategy(data.unidad).from_cm(
                cm_lineales, ancho_cm, por_superficie, data.largo_pieza_cm)
        except ValueError as exc:
            raise UnprocessableError(f"{data.nombre}: {exc}")

    def _cost(self, data, metodo, consumo_cm, consumo_unidad, costo=None, aplicar_merma=True, **extra):
        if aplicar_merma and data.merma_pct:
            factor = 1 + data.merma_pct / 100.0
            consumo_cm *= factor
            consumo_unidad *= factor
        if costo is None:
            costo = round(consumo_unidad * data.precio_unitario, 2)
        return ComponentCost(
            merma_pct=data.merma_pct,
            minutos=data.minutos,
            componente=data.nombre,
            consumo_m_o_m2=round(consumo_unidad, 4),
            unidad=data.unidad,
            consumo_cm=round(consumo_cm, 2),
            medida_corte=self._medida(data),
            precio_unitario=data.precio_unitario,
            costo_parcial=costo,
            metodo=metodo,
            **extra,
        )


class FabricStrategy(CalculationStrategy):
    """Tela cortada del rollo (largo = alto), aprovechando un retazo si alguno alcanza."""

    tipo = 'lineal_alto'
    por_superficie = False

    def calculate(self, data):
        consumo = self._convertir(data, data.alto_corte, data.ancho_corte, self.por_superficie)
        retazo = buscar_retazo(data.retazos, data.ancho_corte, data.alto_corte)
        if retazo:
            # Un retazo ya fue pagado como parte del rollo original: no suma costo
            return self._cost(
                data, "RETAZO", 1.0, consumo, costo=0.0, aplicar_merma=False,
                id_retazo=retazo.id,
                mensaje=f"Usar retazo de {int(retazo.ancho_cm)}x{int(retazo.largo_cm)} cm",
            )
        return self._cost(data, "ROLLO", data.alto_corte, consumo)


class SurfaceFabricStrategy(FabricStrategy):
    """Tela cobrada por superficie (ancho × alto en m²), aprovechando retazos."""

    tipo = 'superficie'
    por_superficie = True


class WidthLinearStrategy(CalculationStrategy):
    """Material continuo que se corta al ancho (cinta, espagueti)."""

    tipo = 'lineal_ancho'

    def calculate(self, data):
        consumo = self._convertir(data, data.ancho_corte, data.ancho_corte, False)
        return self._cost(data, "BARRA", data.ancho_corte, consumo)


class ProfileStrategy(CalculationStrategy):
    """Perfiles y caños que se compran en piezas de largo fijo (2, 4 o 6 m) y se cortan al ancho.

    Cada corte sale de una sola pieza (nunca se empalma): primero del sobrante reutilizable
    más corto que alcance; si no hay, de una pieza nueva. Si el sobrante mide al menos
    `min_retazo_cm` queda como retazo para próximos cortes; si no, se pierde y se cobra.
    `data.retazos` es el conjunto de sobrantes del insumo, compartido entre componentes:
    la estrategia lo actualiza.
    """

    tipo = 'perfil'

    def calculate(self, data):
        corte = round(data.ancho_corte, 2)
        largo_pieza = float(data.largo_pieza_cm or 0)
        if corte <= 0:
            raise UnprocessableError(f"{data.nombre}: la medida de corte debe ser mayor a 0")
        if largo_pieza <= 0:
            raise UnprocessableError(f"{data.nombre}: el perfil no tiene largo_pieza_cm cargado")
        if corte > largo_pieza + 1e-9:
            raise UnprocessableError(
                f"{data.nombre}: el corte de {corte:g} cm no entra en una pieza de {largo_pieza:g} cm. "
                "Un perfil no se empalma: hay que usar uno igual o más largo que el ancho.")

        cantidad = max(1, math.ceil(data.cantidad_base - 1e-9))
        cortes = []
        cm_stock = 0.0
        for _ in range(cantidad):
            origen = self._sobrante_que_alcanza(data.retazos, corte)
            if origen:
                data.retazos.remove(origen)
                usado = origen['largo']
                nuevo = False
            else:
                usado = largo_pieza
                nuevo = True
            sobrante = round(usado - corte, 2)
            reutilizable = sobrante >= data.min_retazo_cm
            tok_sobrante = None
            if reutilizable:
                tok_sobrante = f"s{uuid.uuid4().hex[:8]}"
                data.retazos.append({'id': None, 'tok': tok_sobrante, 'largo': sobrante})
            cm_stock += corte if reutilizable else usado
            cortes.append({
                'origen': 'pieza_nueva' if nuevo else 'retazo',
                'id_pieza': None if nuevo else origen['id'],
                'tok_origen': None if nuevo else origen['tok'],
                'largo_origen': round(usado, 2),
                'corte': corte,
                'sobrante': sobrante,
                'reutilizable': reutilizable,
                'tok_sobrante': tok_sobrante,
                'desperdicio': 0.0 if reutilizable else sobrante,
            })

        consumo = self._convertir(data, cm_stock, data.ancho_corte, False)
        usa_retazo = any(c['origen'] == 'retazo' for c in cortes)
        piezas_nuevas = sum(1 for c in cortes if c['origen'] == 'pieza_nueva')
        mensaje = f"{cantidad} corte(s) de {corte:g} cm: {piezas_nuevas} pieza(s) nueva(s)"
        if usa_retazo:
            mensaje += f", {cantidad - piezas_nuevas} desde sobrante"
        guardados = [c for c in cortes if c['reutilizable']]
        if guardados:
            mensaje += f"; sobrante reutilizable de {guardados[-1]['sobrante']:g} cm"
        perdidos = sum(c['desperdicio'] for c in cortes)
        if perdidos:
            mensaje += f"; se descartan {perdidos:g} cm"
        return self._cost(
            data, "PERFIL", cm_stock, consumo, aplicar_merma=False, cortes=cortes, mensaje=mensaje)

    @staticmethod
    def _sobrante_que_alcanza(retazos, corte):
        candidatos = [r for r in retazos if r['largo'] >= corte]
        return min(candidatos, key=lambda r: r['largo']) if candidatos else None


class FixedStrategy(CalculationStrategy):
    """Cantidad fija por producto (cadenas, soportes, tapas)."""

    tipo = 'fijo'

    def calculate(self, data):
        return self._cost(data, "UNIDAD", data.cantidad_base, data.cantidad_base)


class LaborStrategy(CalculationStrategy):
    """Solo mano de obra: no consume material."""

    tipo = 'mano_obra'

    def calculate(self, data):
        return self._cost(data, "MANO_OBRA", 0.0, 0.0, costo=0.0, aplicar_merma=False)


STRATEGIES = {
    s.tipo: s for s in (
        FabricStrategy(), SurfaceFabricStrategy(), WidthLinearStrategy(),
        ProfileStrategy(), FixedStrategy(), LaborStrategy(),
    )
}


def register_strategy(strategy):
    STRATEGIES[strategy.tipo] = strategy


def get_strategy(tipo):
    try:
        return STRATEGIES[tipo]
    except KeyError:
        raise UnprocessableError(
            f"El tipo de cálculo '{tipo}' de la receta no está soportado",
            detalles=sorted(STRATEGIES),
        )


def usa_retazos(tipo):
    return isinstance(STRATEGIES.get(tipo), FabricStrategy)


def usa_perfiles(tipo):
    return isinstance(STRATEGIES.get(tipo), ProfileStrategy)
