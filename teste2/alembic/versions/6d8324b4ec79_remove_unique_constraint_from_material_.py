"""Remove unique constraint from material name

Revision ID: 6d8324b4ec79
Revises: 00fd8b6c3351
Create Date: 2024-07-31 15:06:02.203979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d8324b4ec79'
down_revision: Union[str, None] = '00fd8b6c3351'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('materiais') as batch_op:
        batch_op.drop_constraint('uq_material_nome', type_='unique')

def downgrade():
    with op.batch_alter_table('materiais') as batch_op:
        batch_op.create_unique_constraint('uq_material_nome', ['nome'])
