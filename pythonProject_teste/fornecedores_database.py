# tecnico_database.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Fornecedor(Base):
    __tablename__ = 'fornecedores'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cnpj = Column(Integer, nullable=False)

# Conecta ao banco de dados
engine = create_engine('sqlite:///fornecedores.db')
Base.metadata.create_all(engine)
