from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    nota_fiscal = Column(String, nullable=True)
    quantidade = Column(Integer, nullable=True)
    fornecedor = Column(String, nullable=True)
    data = Column(Date, nullable=True)

class Estoque(Base):
    __tablename__ = 'estoque'

    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    quantidade = Column(Integer, nullable=False)
    produto = relationship("Produto")

class SaidaMaterial(Base):
    __tablename__ = 'saida_material'

    id = Column(Integer, primary_key=True)
    tecnico = Column(String, nullable=False)
    tipo_saida = Column(String, nullable=False)
    ordem_servico = Column(String, nullable=False)
    data_ordem = Column(Date, nullable=False)
    local_servico = Column(String, nullable=False)
    patrimonio = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    produto = relationship("Produto")

# Função para criar o banco de dados e as tabelas
def criar_banco_dados():
    try:
        engine = create_engine('sqlite:///estoque_database.db')
        Base.metadata.create_all(engine)
        return engine

    except SQLAlchemyError as e:
        print(f"Erro ao criar o banco de dados: {e}")
        raise

# Função para iniciar a sessão do banco de dados
def iniciar_sessao(engine):
    try:
        Session = sessionmaker(bind=engine)
        return Session()
    except Exception as e:
        print(f"Erro ao iniciar a sessão do banco de dados: {e}")
        raise

# Função para registrar um novo produto e atualizar o estoque
def registrar_produto(nome, preco, nota_fiscal, quantidade, fornecedor, data):
    engine = criar_banco_dados()
    session = iniciar_sessao(engine)

    try:
        # Verifica se o produto já existe
        produto_existente = session.query(Produto).filter_by(nome=nome).first()
        if produto_existente:
            print(f"Produto {nome} já está registrado com ID {produto_existente.id}.")
            return

        # Cria e adiciona o novo produto
        novo_produto = Produto(nome=nome, preco=preco, nota_fiscal=nota_fiscal, quantidade=quantidade, fornecedor=fornecedor, data=data)
        session.add(novo_produto)
        session.commit()  # Commit para garantir que o produto tenha um ID

        # Adiciona o produto ao estoque
        novo_estoque = Estoque(produto_id=novo_produto.id, quantidade=quantidade)
        session.add(novo_estoque)
        session.commit()

        print(f"Produto {nome} registrado com sucesso com quantidade inicial {quantidade}!")

    except Exception as e:
        print(f"Erro ao registrar produto: {e}")
        session.rollback()

    finally:
        session.close()

# Função para registrar a saída de material
def registrar_saida_material(produto_id, tecnico, tipo_saida, ordem_servico, data_ordem, local_servico, patrimonio, quantidade):
    engine = criar_banco_dados()
    session = iniciar_sessao(engine)

    try:
        # Verifica se o produto existe no estoque e se a quantidade é suficiente
        estoque = session.query(Estoque).filter_by(produto_id=produto_id).first()
        if estoque is None:
            print("Produto não encontrado no estoque.")
            return

        if estoque.quantidade < quantidade:
            print("Quantidade insuficiente no estoque.")
            return

        # Atualiza a quantidade no estoque
        estoque.quantidade -= quantidade
        session.commit()

        # Registra a saída de material
        saida_material = SaidaMaterial(
            produto_id=produto_id,
            tecnico=tecnico,
            tipo_saida=tipo_saida,
            ordem_servico=ordem_servico,
            data_ordem=data_ordem,
            local_servico=local_servico,
            patrimonio=patrimonio,
            quantidade=quantidade
        )
        session.add(saida_material)
        session.commit()

        print("Saída de material registrada com sucesso.")

    except Exception as e:
        print(f"Erro ao registrar saída de material: {e}")
        session.rollback()

    finally:
        session.close()
