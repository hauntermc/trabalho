from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import date

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

# Conecta ao banco de dados
engine_produto = create_engine('sqlite:///produtos2.db')
Base.metadata.create_all(engine_produto)
