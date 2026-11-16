"""tabla de usuarios con rol

Revision ID: 0002_usuarios
Revises: 0001_indices
Create Date: 2026-11-03
"""
from alembic import op
import sqlalchemy as sa

revision = '0002_usuarios'
down_revision = '0001_indices'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    if 'usuarios' in sa.inspect(bind).get_table_names():
        return
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('rol', sa.String(20), nullable=False),
        sa.Column('activo', sa.Boolean(), nullable=False),
        sa.Column('intentos_fallidos', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('bloqueado_hasta', sa.DateTime()),
        sa.Column('ultimo_login', sa.DateTime()),
        sa.Column('creado_en', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_usuarios_email', 'usuarios', ['email'], unique=True)


def downgrade():
    op.drop_index('ix_usuarios_email', table_name='usuarios')
    op.drop_table('usuarios')
