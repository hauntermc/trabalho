"""Add estoque_minimo to materiais

Revision ID: 7406c4bbd465
Revises: 52dc4c3d99be
Create Date: 2024-07-24 13:50:55.144777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7406c4bbd465'
down_revision: Union[str, None] = '52dc4c3d99be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("UPDATE materiais SET estoque_minimo = 0 WHERE estoque_minimo IS NULL")

    # Adiciona a coluna estoque_minimo à tabela materiais como NULLABLE
    op.add_column('materiais', sa.Column('estoque_minimo', sa.Integer(), nullable=True))


def downgrade():
    # Remove a coluna estoque_minimo da tabela materiais
    op.drop_column('materiais', 'estoque_minimo')
