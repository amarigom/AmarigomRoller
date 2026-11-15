"""Copia controlada de datos de desarrollo a una rama nueva de PostgreSQL."""
import os

from alembic import command
from alembic.config import Config
from sqlalchemy import MetaData, Table, create_engine, func, inspect, select, text
from sqlalchemy.engine import make_url

from config import Config as AppConfig
from exceptions import ConflictError, ValidationFailed

_TABLAS_COPIAR = (
    'usuarios', 'insumos', 'clientes', 'productos', 'recetas', 'receta_items',
    'inventario_movimientos', 'historial_precios_insumos', 'retazos_telas',
)
_VACIAS = tuple(t for t in _TABLAS_COPIAR if t != 'insumos') + ('producciones',)
_VERIFICAR = ('categorias_insumos', 'rollos', 'stock_piezas_detalle')
_CANTIDADES_ORIGEN = {
    'usuarios': 3, 'insumos': 35, 'clientes': 8, 'productos': 3, 'recetas': 4,
    'receta_items': 24, 'inventario_movimientos': 35, 'historial_precios_insumos': 35,
    'retazos_telas': 1,
}


def _tabla(connection, nombre):
    return Table(nombre, MetaData(), autoload_with=connection)


def _filas(connection, tabla):
    return {row['id']: dict(row) for row in connection.execute(select(tabla)).mappings()}


def _comparar_identidad(origen, destino, tablas):
    for nombre in _VERIFICAR:
        izquierda, derecha = tablas[nombre]
        cols = set(izquierda.c.keys()) & set(derecha.c.keys())
        if nombre == 'stock_piezas_detalle':
            cols.discard('fecha_ingreso')
        a = {i: {k: v for k, v in row.items() if k in cols} for i, row in _filas(origen, izquierda).items()}
        b = {i: {k: v for k, v in row.items() if k in cols} for i, row in _filas(destino, derecha).items()}
        if a != b:
            raise ConflictError(f'{nombre} difiere entre ramas; revisá los datos antes de continuar')


def sincronizar_desarrollo(apply=False):
    source_url = os.environ.get('DEV_DATABASE_URL')
    target_url = AppConfig.SQLALCHEMY_DATABASE_URI
    if not source_url or not target_url:
        raise ValidationFailed('Configurá DEV_DATABASE_URL y DATABASE_URL en el entorno local')
    source_url = source_url.replace('postgres://', 'postgresql://', 1)
    target_url = target_url.replace('postgres://', 'postgresql://', 1)
    a, b = make_url(source_url), make_url(target_url)
    if a.get_backend_name() != 'postgresql' or b.get_backend_name() != 'postgresql':
        raise ValidationFailed('La sincronización requiere dos bases PostgreSQL')
    if (a.host, a.database) == (b.host, b.database):
        raise ValidationFailed('Origen y destino podrían ser la misma base; operación cancelada')

    source_engine, target_engine = create_engine(a), create_engine(b)
    try:
        with source_engine.connect() as source, target_engine.connect() as target:
            source.execute(text('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY'))
            target.execute(text('SET LOCAL lock_timeout = :timeout'), {'timeout': '10s'})
            nombres = sorted(set(_TABLAS_COPIAR + _VERIFICAR + ('producciones', 'recetas_bom', 'alembic_version')))
            for name in nombres:
                target.execute(text(f'LOCK TABLE "{name}" IN SHARE ROW EXCLUSIVE MODE'))
            source_revision = source.execute(text('SELECT version_num FROM alembic_version')).scalars().all()
            target_revision = target.execute(text('SELECT version_num FROM alembic_version')).scalars().all()
            if source_revision != ['0008_etiqueta_desgaste'] or target_revision not in (
                    ['6b0584b28197'], ['0011_compatibilidad_legacy']):
                raise ConflictError('Las revisiones de las bases cambiaron; volvé a auditar antes de sincronizar')

            for nombre, cantidad in _CANTIDADES_ORIGEN.items():
                if source.execute(text(f'SELECT count(*) FROM "{nombre}"')).scalar_one() != cantidad:
                    raise ConflictError(f'{nombre} cambió en el origen; volvé a revisar el plan')
            for nombre, cantidad in (('insumos', 32), ('recetas_bom', 4)):
                if target.execute(text(f'SELECT count(*) FROM "{nombre}"')).scalar_one() != cantidad:
                    raise ConflictError(f'{nombre} cambió en el destino; volvé a revisar el plan')
            for nombre in _VACIAS:
                if target.execute(text(f'SELECT count(*) FROM "{nombre}"')).scalar_one():
                    raise ConflictError(f'{nombre} ya contiene datos en el destino; no se sobrescribirá')
            if source.execute(text('SELECT count(*) FROM producciones')).scalar_one():
                raise ConflictError('El origen tiene producciones; se requiere otro plan para conservar sus referencias')

            migration_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'migrations')
            cfg = Config(os.path.join(migration_dir, 'alembic.ini'))
            cfg.set_main_option('script_location', migration_dir)
            cfg.attributes['connection'] = target
            command.upgrade(cfg, '0011_compatibilidad_legacy')

            tablas = {name: (_tabla(source, name), _tabla(target, name))
                      for name in set(_TABLAS_COPIAR + _VERIFICAR)}
            _comparar_identidad(source, target, tablas)
            origen, destino = tablas['insumos']
            filas_origen, filas_destino = _filas(source, origen), _filas(target, destino)
            if not filas_destino.keys() <= filas_origen.keys():
                raise ConflictError('Hay insumos nuevos en destino; no se sobrescribirán')
            for id_, row in filas_destino.items():
                previo = filas_origen[id_]
                if (row['codigo_sku'], row['name'], row['categoria_id']) != (
                        previo['codigo_sku'], previo['name'], previo['categoria_id']):
                    raise ConflictError('La identidad de los insumos cambió; no se sobrescribirán')
                if row['es_tela'] or any(row[k] is not None for k in ('precio_m2', 'unidad_compra', 'factor_conversion')):
                    raise ConflictError('Hay configuración nueva de tela en destino; no se sobrescribirá')

            resumen = {}
            for nombre in _TABLAS_COPIAR:
                original, actual = tablas[nombre]
                columnas = set(original.c.keys()) & set(actual.c.keys())
                filas = [{key: value for key, value in row.items() if key in columnas}
                         for row in source.execute(select(original)).mappings()]
                if nombre == 'insumos':
                    for row in filas:
                        if row['id'] in filas_destino:
                            datos = {k: v for k, v in row.items() if k != 'id'}
                            target.execute(actual.update().where(actual.c.id == row['id']).values(**datos))
                        else:
                            target.execute(actual.insert().values(**row))
                    resumen[nombre] = len(filas)
                else:
                    if filas:
                        target.execute(actual.insert(), filas)
                    resumen[nombre] = len(filas)

            for nombre in _TABLAS_COPIAR:
                original, actual = tablas[nombre]
                columnas = set(original.c.keys()) & set(actual.c.keys())
                anteriores = _filas(source, original)
                copiadas = _filas(target, actual)
                if anteriores.keys() != copiadas.keys() or any(
                        any(row[k] != copiadas[id_][k] for k in columnas)
                        for id_, row in anteriores.items()):
                    raise ConflictError(f'La verificación de {nombre} no coincide; no se confirmó la copia')

            if apply:
                for nombre in _TABLAS_COPIAR:
                    sequence = target.execute(text(
                        "SELECT format('%I.%I', n.nspname, s.relname) "
                        "FROM pg_class s JOIN pg_namespace n ON n.oid=s.relnamespace "
                        "WHERE s.oid=pg_get_serial_sequence(:tabla, 'id')::regclass"),
                        {'tabla': nombre}).scalar_one_or_none()
                    if sequence:
                        current_max = target.execute(select(func.coalesce(func.max(tablas[nombre][1].c.id), 0))).scalar_one()
                        target.execute(text(f'ALTER SEQUENCE {sequence} RESTART WITH {int(current_max) + 1}'))
                target.commit()
            else:
                target.rollback()
            source.rollback()
            return resumen
    finally:
        source_engine.dispose()
        target_engine.dispose()
