"""Adicionar coluna devolvido na tabela retirada_material

Revision ID: nova_revision_id
Revises: 886922d316b4
Create Date: 2024-07-19 15:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'nova_revision_id'
down_revision: Union[str, None] = '886922d316b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Verifica se a coluna 'devolvido' já existe
    inspector = sa.inspect(op.get_bind())
    columns = [col['name'] for col in inspector.get_columns('retirada_material')]

    if 'devolvido' not in columns:
        op.add_column('retirada_material', sa.Column('devolvido', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')))

def downgrade() -> None:
    # Remove a coluna devolvido se ela existir
    inspector = sa.inspect(op.get_bind())
    columns = [col['name'] for col in inspector.get_columns('retirada_material')]

    if 'devolvido' in columns:
        op.drop_column('retirada_material', 'devolvido')
