"""Estrategias de cálculo de consumo y costo según el `tipo_calculo` de cada componente de la receta.

Para sumar un tipo nuevo basta con crear una subclase de CalculationStrategy y
registrarla en STRATEGIES (o con register_strategy).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from exceptions import UnprocessableError
from strategies.units import get_unit_strategy


@dataclass
class ComponentInput:
    nombre: str
    unidad: str
    precio_unitario: float
    ancho_corte: float
    alto_corte: float
    cantidad_base: float = 1.0
    retazos: list = field(default_factory=list)


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

    def _cost(self, data, metodo, consumo_cm, consumo_unidad, costo=None, **extra):
        if costo is None:
            costo = round(consumo_unidad * data.precio_unitario, 2)
        return ComponentCost(
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
        unidad = get_unit_strategy(data.unidad)
        consumo = unidad.from_cm(data.alto_corte, data.ancho_corte, self.por_superficie)
        retazo = buscar_retazo(data.retazos, data.ancho_corte, data.alto_corte)
        if retazo:
            # Un retazo ya fue pagado como parte del rollo original: no suma costo
            return self._cost(
                data, "RETAZO", 1.0, consumo, costo=0.0,
                id_retazo=retazo.id,
                mensaje=f"Usar retazo de {int(retazo.ancho_cm)}x{int(retazo.largo_cm)} cm",
            )
        return self._cost(data, "ROLLO", data.alto_corte, consumo)


class SurfaceFabricStrategy(FabricStrategy):
    tipo = 'superficie'
    por_superficie = True


class WidthLinearStrategy(CalculationStrategy):
    """Barras o perfiles que se cortan al ancho."""

    tipo = 'lineal_ancho'

    def calculate(self, data):
        consumo = get_unit_strategy(data.unidad).from_cm(data.ancho_corte, data.ancho_corte, False)
        return self._cost(data, "BARRA", data.ancho_corte, consumo)


class FixedStrategy(CalculationStrategy):
    """Cantidad fija por producto (cadenas, soportes, tapas)."""

    tipo = 'fijo'

    def calculate(self, data):
        return self._cost(data, "UNIDAD", data.cantidad_base, data.cantidad_base)


STRATEGIES = {
    s.tipo: s for s in (FabricStrategy(), SurfaceFabricStrategy(), WidthLinearStrategy(), FixedStrategy())
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
