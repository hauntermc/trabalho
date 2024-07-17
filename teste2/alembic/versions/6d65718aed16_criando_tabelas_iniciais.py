"""Criando tabelas iniciais

Revision ID: 6d65718aed16
Revises: <coloque_aqui_o_ID_da_revisao_anterior_caso_haja>
Create Date: 2024-07-17 11:25:17.480819

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d65718aed16'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Verifica se a tabela temporária 'materiais_temp' já existe
    if not inspector.has_table('materiais_temp'):
        # Cria a tabela 'materiais_temp' com a mesma estrutura de 'materiais'
        op.create_table('materiais_temp',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('nome', sa.String(), nullable=False),
            sa.Column('preco', sa.Float(), nullable=False),
            sa.Column('nota_fiscal', sa.String(), nullable=False),
            sa.Column('quantidade', sa.Integer(), nullable=False),
            sa.Column('fornecedor', sa.String(), nullable=False),
            sa.Column('data', sa.Date(), nullable=False)
        )

        # Copia os dados de 'materiais' para 'materiais_temp'
        op.execute('INSERT INTO materiais_temp (id, nome, preco, nota_fiscal, quantidade, fornecedor, data) '
                    'SELECT id, nome, preco, nota_fiscal, quantidade, fornecedor, data FROM materiais')

        # Exclui a tabela original 'materiais'
        op.drop_table('materiais')

        # Renomeia 'materiais_temp' para 'materiais'
        op.rename_table('materiais_temp', 'materiais')

def downgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Verifica se a tabela 'materiais' já existe (pode ser útil para downgrade)
    if not inspector.has_table('materiais'):
        op.create_table('materiais',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('nome', sa.String(), nullable=False),
            sa.Column('preco', sa.Float(), nullable=False),
            sa.Column('nota_fiscal', sa.String(), nullable=False),
            sa.Column('quantidade', sa.Integer(), nullable=False),
            sa.Column('fornecedor', sa.String(), nullable=False),
            sa.Column('data', sa.Date(), nullable=False)
        )

        # Copia os dados de 'materiais_temp' de volta para 'materiais'
        op.execute('INSERT INTO materiais (id, nome, preco, nota_fiscal, quantidade, fornecedor, data) '
                    'SELECT id, nome, preco, nota_fiscal, quantidade, fornecedor, data FROM materiais_temp')

        # Exclui a tabela temporária 'materiais_temp'
        op.drop_table('materiais_temp')
