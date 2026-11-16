"""Estrategias de conversión: pasan cm lineales a la unidad en que está cargado el precio y el stock del insumo."""
from abc import ABC, abstractmethod


class UnitStrategy(ABC):
    nombres = ()

    @abstractmethod
    def from_cm(self, cm_lineales, ancho_cm, por_superficie, largo_pieza_cm=None):
        """Devuelve el consumo expresado en la unidad del insumo."""


class CentimeterUnit(UnitStrategy):
    """cm: el consumo queda en cm."""
    nombres = ('cm', 'centimetro', 'centimetros')

    def from_cm(self, cm_lineales, ancho_cm, por_superficie, largo_pieza_cm=None):
        return cm_lineales


class MeterUnit(UnitStrategy):
    nombres = ('metro', 'metros', 'm', 'mt', 'mts', 'ml')

    def from_cm(self, cm_lineales, ancho_cm, por_superficie, largo_pieza_cm=None):
        return cm_lineales / 100.0


class SquareMeterUnit(UnitStrategy):
    nombres = ('m2', 'm²')

    def from_cm(self, cm_lineales, ancho_cm, por_superficie, largo_pieza_cm=None):
        if por_superficie:
            return (ancho_cm * cm_lineales) / 10000.0
        return cm_lineales / 100.0


class PieceUnit(UnitStrategy):
    """Rollo o pieza entera con largo conocido (cinta de 50 m): el consumo es la fracción usada."""
    nombres = ('rollo', 'rollos', 'pieza', 'piezas')

    def from_cm(self, cm_lineales, ancho_cm, por_superficie, largo_pieza_cm=None):
        if not largo_pieza_cm:
            raise ValueError("El insumo se mide en rollos/piezas pero no tiene largo_pieza_cm cargado")
        return cm_lineales / float(largo_pieza_cm)


class PassThroughUnit(UnitStrategy):
    """unidad u otras: el consumo queda en cm."""

    def from_cm(self, cm_lineales, ancho_cm, por_superficie, largo_pieza_cm=None):
        return cm_lineales


_DEFAULT = PassThroughUnit()
_REGISTRY = {
    nombre: s
    for s in (CentimeterUnit(), MeterUnit(), SquareMeterUnit(), PieceUnit())
    for nombre in s.nombres
}


def get_unit_strategy(nombre):
    return _REGISTRY.get((nombre or '').strip().lower(), _DEFAULT)
