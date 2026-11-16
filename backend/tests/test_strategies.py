import pytest

from exceptions import UnprocessableError
from strategies.costing import STRATEGIES, CalculationStrategy, ComponentCost, get_strategy, register_strategy
from strategies.notifications import LogNotifier, ResendNotifier, create_notifier
from strategies.units import get_unit_strategy


def test_conversion_unidades():
    assert get_unit_strategy('metro').from_cm(200, 100, False) == 2.0
    assert get_unit_strategy('MTS').from_cm(200, 100, False) == 2.0
    assert get_unit_strategy('cm').from_cm(200, 100, False) == 200
    assert get_unit_strategy('m2').from_cm(200, 100, True) == 2.0
    assert get_unit_strategy('m2').from_cm(200, 100, False) == 2.0


def test_registro_de_estrategias():
    assert {'lineal_alto', 'superficie', 'lineal_ancho', 'fijo'} <= set(STRATEGIES)
    with pytest.raises(UnprocessableError):
        get_strategy('desconocido')


def test_se_puede_registrar_una_estrategia_nueva():
    class Doble(CalculationStrategy):
        tipo = 'doble_test'

        def calculate(self, data):
            return ComponentCost(data.nombre, 2, data.unidad, 2, '', 1, 2, 'DOBLE')

    register_strategy(Doble())
    try:
        assert get_strategy('doble_test').calculate(type('D', (), {'nombre': 'x', 'unidad': 'u'})()).metodo == 'DOBLE'
    finally:
        STRATEGIES.pop('doble_test')


def test_factory_de_notificador():
    assert isinstance(create_notifier({}), LogNotifier)
    n = create_notifier({'RESEND_API_KEY': 'k', 'MAIL_DEFAULT_SENDER': 'a@b.com'})
    assert isinstance(n, ResendNotifier)
