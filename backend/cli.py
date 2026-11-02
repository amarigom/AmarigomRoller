import click
from flask.cli import with_appcontext

import container
from schemas.auth import MIN_PASSWORD_LENGTH


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


def register_cli(app):
    app.cli.add_command(create_admin)
