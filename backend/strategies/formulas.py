"""Evaluador seguro de fórmulas y condiciones de recetas ('ancho + 5', 'ceil(ancho / 100)', "ancho > 200 and sistema == 'motor'").

Solo se aceptan números, textos, variables, operadores aritméticos y de comparación, and/or/not,
condicionales (a if c else b) y unas pocas funciones. Cualquier otro nodo se rechaza: nunca se usa eval.
"""
import ast
import math
import operator

MAX_LARGO = 200
MAX_NODOS = 60

FUNCIONES = {
    'ceil': math.ceil,
    'floor': math.floor,
    'round': round,
    'min': min,
    'max': max,
    'abs': abs,
}

_BINARIOS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
}
_COMPARACIONES = {
    ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Lt: operator.lt,
    ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge,
}


class FormulaError(ValueError):
    pass


def compilar(texto):
    """Parsea y valida la sintaxis. Devuelve el árbol listo para evaluar."""
    if not isinstance(texto, str) or not texto.strip():
        raise FormulaError("La fórmula está vacía")
    if len(texto) > MAX_LARGO:
        raise FormulaError(f"La fórmula supera los {MAX_LARGO} caracteres")
    try:
        arbol = ast.parse(texto.strip(), mode='eval')
    except SyntaxError as exc:
        raise FormulaError(f"Sintaxis inválida en '{texto}'") from exc
    nodos = list(ast.walk(arbol))
    if len(nodos) > MAX_NODOS:
        raise FormulaError("La fórmula es demasiado compleja")
    for nodo in nodos:
        _verificar(nodo)
    return arbol


def _verificar(nodo):
    permitidos = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare, ast.IfExp,
        ast.Call, ast.Name, ast.Constant, ast.Load, ast.And, ast.Or, ast.Not, ast.USub, ast.UAdd,
        *_BINARIOS, *_COMPARACIONES,
    )
    if not isinstance(nodo, permitidos):
        raise FormulaError(f"Operación no permitida: {type(nodo).__name__}")
    if isinstance(nodo, ast.Constant) and not isinstance(nodo.value, (int, float, str, bool)):
        raise FormulaError("Solo se permiten números y textos")
    if isinstance(nodo, ast.Call):
        if not isinstance(nodo.func, ast.Name) or nodo.func.id not in FUNCIONES or nodo.keywords:
            raise FormulaError(f"Función no permitida (disponibles: {', '.join(sorted(FUNCIONES))})")


def variables(arbol):
    """Nombres de variables usados (sin contar las funciones)."""
    llamadas = {n.func.id for n in ast.walk(arbol) if isinstance(n, ast.Call)}
    return {n.id for n in ast.walk(arbol) if isinstance(n, ast.Name)} - llamadas


def evaluar(texto, contexto):
    """Evalúa la fórmula con las variables de `contexto`. Una variable inexistente vale None."""
    return _evaluar(compilar(texto).body, contexto)


def _evaluar(nodo, ctx):
    if isinstance(nodo, ast.Constant):
        return nodo.value
    if isinstance(nodo, ast.Name):
        return ctx.get(nodo.id)
    if isinstance(nodo, ast.UnaryOp):
        valor = _evaluar(nodo.operand, ctx)
        if isinstance(nodo.op, ast.Not):
            return not valor
        return -_numero(valor) if isinstance(nodo.op, ast.USub) else _numero(valor)
    if isinstance(nodo, ast.BinOp):
        try:
            return _BINARIOS[type(nodo.op)](_numero(_evaluar(nodo.left, ctx)), _numero(_evaluar(nodo.right, ctx)))
        except ZeroDivisionError as exc:
            raise FormulaError("División por cero") from exc
    if isinstance(nodo, ast.BoolOp):
        valores = (_evaluar(v, ctx) for v in nodo.values)
        return all(valores) if isinstance(nodo.op, ast.And) else any(valores)
    if isinstance(nodo, ast.Compare):
        izq = _evaluar(nodo.left, ctx)
        for op, der_nodo in zip(nodo.ops, nodo.comparators):
            der = _evaluar(der_nodo, ctx)
            try:
                if not _COMPARACIONES[type(op)](izq, der):
                    return False
            except TypeError:
                return False  # comparar un número con una opción no cargada (None) da falso
            izq = der
        return True
    if isinstance(nodo, ast.IfExp):
        return _evaluar(nodo.body if _evaluar(nodo.test, ctx) else nodo.orelse, ctx)
    if isinstance(nodo, ast.Call):
        args = [_numero(_evaluar(a, ctx)) for a in nodo.args]
        try:
            return FUNCIONES[nodo.func.id](*args)
        except (TypeError, ValueError) as exc:
            raise FormulaError(f"Argumentos inválidos en {nodo.func.id}()") from exc
    raise FormulaError("Expresión no soportada")


def _numero(valor):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise FormulaError("La fórmula necesita un valor numérico (¿falta una opción?)")
    return valor


def evaluar_numero(texto, contexto):
    return float(_numero(evaluar(texto, contexto)))


def evaluar_condicion(texto, contexto):
    return bool(evaluar(texto, contexto))
