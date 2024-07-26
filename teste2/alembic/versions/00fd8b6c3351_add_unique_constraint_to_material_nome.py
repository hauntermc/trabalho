"""Add unique constraint to Material nome

Revision ID: 00fd8b6c3351
Revises: 7406c4bbd465
Create Date: 2024-07-24

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '00fd8b6c3351'
down_revision = '7406c4bbd465'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('materiais', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_material_nome', ['nome'])


def downgrade():
    with op.batch_alter_table('materiais', schema=None) as batch_op:
        batch_op.drop_constraint('uq_material_nome', type_='unique')
