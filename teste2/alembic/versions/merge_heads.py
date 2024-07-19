"""Mesclar cabeças de revisão

Revision ID: merge_123456
Revises: (nova_revision_id, some_unique_revision_id)
Create Date: 2024-07-19 15:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'merge_123456'
down_revision: Union[str, None] = ('nova_revision_id', 'some_unique_revision_id')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Nenhum comando específico necessário
    pass

def downgrade() -> None:
    # Nenhum comando específico necessário
    pass
