from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    preco = Column(Float)

# Conecta ao banco de dados
engine_produto = create_engine('sqlite:///produtos.db')
Base.metadata.create_all(engine_produto)
