"""Estrategias de conversión: pasan cm lineales a la unidad en que está cargado el precio del insumo."""
from abc import ABC, abstractmethod


class UnitStrategy(ABC):
    nombres = ()

    @abstractmethod
    def from_cm(self, cm_lineales, ancho_cm, por_superficie):
        """Devuelve el consumo expresado en la unidad del insumo."""


class MeterUnit(UnitStrategy):
    nombres = ('metro', 'metros', 'm', 'mt', 'mts', 'ml')

    def from_cm(self, cm_lineales, ancho_cm, por_superficie):
        return cm_lineales / 100.0


class SquareMeterUnit(UnitStrategy):
    nombres = ('m2', 'm²')

    def from_cm(self, cm_lineales, ancho_cm, por_superficie):
        if por_superficie:
            return (ancho_cm * cm_lineales) / 10000.0
        return cm_lineales / 100.0


class PassThroughUnit(UnitStrategy):
    """cm, unidad u otras: el consumo queda en cm."""

    def from_cm(self, cm_lineales, ancho_cm, por_superficie):
        return cm_lineales


_DEFAULT = PassThroughUnit()
_REGISTRY = {nombre: s for s in (MeterUnit(), SquareMeterUnit()) for nombre in s.nombres}


def get_unit_strategy(nombre):
    return _REGISTRY.get((nombre or '').strip().lower(), _DEFAULT)
