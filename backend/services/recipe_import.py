"""Lectura de recetas desde CSV (exportado de Excel). Sin acceso a base de datos."""
import csv
import io

from pydantic import ValidationError

from schemas.recipes import RecipeItemIn

MAX_FILAS = 2000
COLUMNAS = ['producto', *RecipeItemIn.model_fields]
OBLIGATORIAS = {'producto', 'nombre', 'tipo_calculo'}
NUMERICAS = {'delta_ancho_cm', 'delta_alto_cm', 'cantidad_base', 'merma_pct', 'minutos_mano_obra', 'id_insumo'}


def plantilla():
    """Encabezado para que el equipo arme la planilla."""
    return ';'.join(COLUMNAS) + '\n'


def _delimitador(texto):
    primera = texto.splitlines()[0] if texto.splitlines() else ''
    return ';' if primera.count(';') >= primera.count(',') else ','


def _numero(valor):
    # Excel en español exporta con coma decimal
    return valor.replace(',', '.') if valor.count(',') == 1 and '.' not in valor else valor


def parsear(texto):
    """Devuelve ({producto: [RecipeItemIn]}, [errores]). Los errores indican la fila del archivo."""
    texto = texto.lstrip('\ufeff')
    lector = csv.DictReader(io.StringIO(texto), delimiter=_delimitador(texto))
    columnas = {(c or '').strip().lower() for c in (lector.fieldnames or [])}
    faltan = OBLIGATORIAS - columnas
    if faltan:
        return {}, [f"Faltan columnas obligatorias: {', '.join(sorted(faltan))}"]
    desconocidas = columnas - set(COLUMNAS)
    if desconocidas:
        return {}, [f"Columnas desconocidas: {', '.join(sorted(desconocidas))}"]

    productos, errores = {}, []
    for n, fila in enumerate(lector, start=2):
        if n - 1 > MAX_FILAS:
            return {}, [f"El archivo supera las {MAX_FILAS} filas"]
        datos = {(k or '').strip().lower(): (v or '').strip() for k, v in fila.items() if k}
        if not any(datos.values()):
            continue
        producto = datos.pop('producto', '')
        if not producto:
            errores.append(f"Fila {n}: falta el producto")
            continue
        limpio = {}
        for campo, valor in datos.items():
            if valor == '':
                continue
            if campo == 'insumos_alternativos':
                limpio[campo] = [x.strip() for x in valor.split('|') if x.strip()]
                continue
            limpio[campo] = _numero(valor) if campo in NUMERICAS else valor
        try:
            productos.setdefault(producto, []).append(RecipeItemIn.model_validate(limpio))
        except ValidationError as exc:
            for err in exc.errors():
                errores.append(f"Fila {n}, {'.'.join(str(p) for p in err['loc'])}: {err['msg']}")
    if not productos and not errores:
        errores.append("El archivo no tiene filas de recetas")
    return productos, errores
