import click
import json
from flask.cli import with_appcontext

import container
from exceptions import AppError
from extensions import db
from schemas.auth import MIN_PASSWORD_LENGTH


@click.command('sincronizar-precios-sheets')
@with_appcontext
def sincronizar_precios_sheets():
    """Actualiza los precios desde Google Sheets."""
    from services.google_sheets_prices import sincronizar_precios
    try:
        resultado = sincronizar_precios()
    except AppError as exc:
        raise click.ClickException(exc.message) from exc
    click.echo(f"Precios actualizados: {resultado['actualizados']}; artículos omitidos: {resultado['omitidos']}")


@click.command('create-admin')
@click.option('--email', prompt=True)
@click.option('--nombre', prompt=True)
@click.password_option()
@with_appcontext
def create_admin(email, nombre, password):
    """Crea un usuario administrador (para el primer acceso)."""
    if len(password) < MIN_PASSWORD_LENGTH:
        raise click.ClickException(f"La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres")
    user = container.user_service().create_admin(email, nombre, password)
    click.echo(f"Administrador creado: {user.email}")


@click.command('seed-demo-fabricacion')
@click.option('--apply', is_flag=True, help='Inserta datos ficticios; sin esta opción solo muestra el plan.')
@with_appcontext
def seed_demo_fabricacion(apply):
    """Prepara datos de prueba sin borrar ni reemplazar registros existentes."""
    click.echo('DEMO: tela de 300 cm/30 m con precio por metro, tres perfiles de 400 cm y dos recetas.')
    if not apply:
        click.echo('Simulación: no se modificó la base. Usá --apply para insertar los datos ficticios.')
        return
    from services.demo_fabricacion import cargar_demo
    try:
        cargar_demo()
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo('Datos DEMO insertados.')


@click.command('normalizar-inventario-inicial')
@click.option('--apply', is_flag=True, help='Aplica el plan; por defecto solo simula.')
@with_appcontext
def normalizar_inventario_inicial(apply):
    """Convierte telas de cm a metros y registra la apertura faltante de etiqueta."""
    from services.normalizacion_inicial import normalizar_inicial
    try:
        plan = normalizar_inicial(aplicar=apply)
        if not apply:
            db.session.rollback()
    except AppError as exc:
        db.session.rollback()
        raise click.ClickException(exc.message) from exc
    for linea in plan:
        click.echo(linea)
    click.echo('Cambios aplicados.' if apply else 'Simulación: no se modificó la base.')


@click.command('preparar-telas-lineales')
@click.option('--apply', is_flag=True, help='Confirma la normalización y las recetas; por defecto simula.')
@with_appcontext
def preparar_telas_lineales(apply):
    """Normaliza telas y publica versiones lineales sin alterar recetas anteriores."""
    from services.telas_lineales import preparar_telas_lineales as preparar
    try:
        plan = preparar(aplicar=apply)
    except AppError as exc:
        db.session.rollback()
        detalles = '; '.join(exc.detalles)
        raise click.ClickException(f'{exc.message}: {detalles}' if detalles else exc.message) from exc
    for linea in plan:
        click.echo(linea)
    click.echo('Cambios aplicados.' if apply else 'Simulación: no se modificó la base.')


@click.command('conciliar-piezas')
@click.argument('archivo', type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option('--apply', is_flag=True, help='Aplica el archivo; por defecto solo simula.')
@with_appcontext
def conciliar_piezas(archivo, apply):
    """Concilia perfiles desde una lista JSON de snapshots y piezas contadas."""
    from schemas.common import parse_payload
    from schemas.inventory import ProfileReconcileIn
    try:
        with open(archivo, encoding='utf-8-sig') as fichero:
            entradas = json.load(fichero)
        if not isinstance(entradas, list) or not entradas:
            raise click.ClickException('El archivo debe contener una lista no vacía')
        ids = [e.get('id_insumo') for e in entradas if isinstance(e, dict)]
        if len(ids) != len(entradas) or any(type(i) is not int or i <= 0 for i in ids) or len(set(ids)) != len(ids):
            raise click.ClickException('Cada entrada debe tener un id_insumo entero y único')
        resultado = []
        servicio = container.inventory_service()
        for entrada in sorted(entradas, key=lambda e: e['id_insumo']):
            datos = parse_payload(ProfileReconcileIn, entrada)
            movimiento = servicio.conciliar_piezas(entrada['id_insumo'], datos, commit=False)
            resultado.append(f"Insumo {entrada['id_insumo']}: ajuste {movimiento.cantidad}, saldo {movimiento.stock_resultante}")
        if apply:
            db.session.commit()
        else:
            db.session.rollback()
    except (OSError, json.JSONDecodeError, AppError, click.ClickException) as exc:
        db.session.rollback()
        raise click.ClickException(str(exc.message if isinstance(exc, AppError) else exc)) from exc
    for linea in resultado:
        click.echo(linea)
    click.echo('Cambios aplicados.' if apply else 'Simulación: no se modificó la base.')


@click.command('sincronizar-desarrollo')
@click.option('--apply', is_flag=True, help='Confirma los cambios; por defecto se revierten.')
@with_appcontext
def sincronizar_desarrollo(apply):
    """Sincroniza una rama destino vacía con los datos existentes de desarrollo."""
    from sqlalchemy.exc import SQLAlchemyError
    from services.sincronizar_desarrollo import sincronizar_desarrollo as sincronizar
    try:
        resumen = sincronizar(apply)
    except AppError as exc:
        raise click.ClickException(exc.message) from exc
    except SQLAlchemyError as exc:
        raise click.ClickException(
            f'La base rechazó la operación ({type(exc.orig).__name__ if exc.orig else type(exc).__name__}); '
            'no se confirmaron cambios. Revisá el esquema antes de reintentar.'
        ) from exc
    for nombre, cantidad in resumen.items():
        click.echo(f'{nombre}: {cantidad} registros de origen')
    click.echo('Cambios aplicados.' if apply else 'Simulación: transacción revertida; no se modificó la base.')


def register_cli(app):
    app.cli.add_command(sincronizar_precios_sheets)
    app.cli.add_command(create_admin)
    app.cli.add_command(seed_demo_fabricacion)
    app.cli.add_command(normalizar_inventario_inicial)
    app.cli.add_command(preparar_telas_lineales)
    app.cli.add_command(conciliar_piezas)
    app.cli.add_command(sincronizar_desarrollo)
