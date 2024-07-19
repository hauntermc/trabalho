from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'some_unique_revision_id'
down_revision = '886922d316b4'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'retorno_material',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('ordem_servico', sa.String(length=50), nullable=False),
        sa.Column('produto_id', sa.Integer, sa.ForeignKey('materiais.id'), nullable=False),
        sa.Column('quantidade', sa.Integer, nullable=False),
        sa.Column('data_retorno', sa.DateTime, default=sa.func.now(), nullable=False),
        sa.Column('data', sa.DateTime, nullable=False),
        sa.Column('tecnico_id', sa.Integer, sa.ForeignKey('tecnicos.id'), nullable=False)
    )

def downgrade():
    op.drop_table('retorno_material')
