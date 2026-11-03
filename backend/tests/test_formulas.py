import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from strategies.formulas import FormulaError, compilar, evaluar, evaluar_condicion, evaluar_numero, variables

CTX = {'ancho': 150.0, 'alto': 200.0, 'sistema': 'motor', 'color': 'blanco'}


@pytest.mark.parametrize("texto, esperado", [
    ("ancho + 5", 155.0),
    ("ancho - 1.5", 148.5),
    ("alto * 2", 400.0),
    ("ceil(ancho / 100)", 2),
    ("floor(ancho / 100)", 1),
    ("max(ancho, alto) - min(ancho, alto)", 50.0),
    ("round(ancho / 7)", 21),
    ("-ancho + 200", 50.0),
    ("2 if ancho > 200 else 1", 1),
    ("ancho // 100 + ancho % 100", 51.0),
])
def test_formulas_validas(texto, esperado):
    assert evaluar_numero(texto, CTX) == esperado


@pytest.mark.parametrize("texto, esperado", [
    ("ancho > 200", False),
    ("ancho > 100 and alto >= 200", True),
    ("sistema == 'motor'", True),
    ("sistema == 'cadena' or color == 'blanco'", True),
    ("not (sistema == 'motor')", False),
    ("100 < ancho < 200", True),
    ("accesorio == 'x'", False),
    ("ancho > accesorio", False),
])
def test_condiciones(texto, esperado):
    assert evaluar_condicion(texto, CTX) is esperado


@pytest.mark.parametrize("texto", [
    "__import__('os').system('echo hola')",
    "open('x')",
    "ancho.__class__",
    "[x for x in range(10)]",
    "lambda: 1",
    "ancho ** 99999999",
    "(1).real",
    "ancho; 1",
    "eval('1')",
    "ancho[0]",
    "{'a': 1}",
    "min(key=len)",
    "x := 5",
    "",
    "   ",
    "ancho +",
    "9" * 300,
])
def test_formulas_peligrosas_o_invalidas_se_rechazan(texto):
    with pytest.raises(FormulaError):
        evaluar(texto, CTX)


def test_division_por_cero_y_opcion_faltante():
    with pytest.raises(FormulaError):
        evaluar_numero("ancho / 0", CTX)
    with pytest.raises(FormulaError):
        evaluar_numero("ancho + faltante", CTX)


def test_variables_usadas():
    assert variables(compilar("ceil(ancho / 100) + largo")) == {'ancho', 'largo'}
