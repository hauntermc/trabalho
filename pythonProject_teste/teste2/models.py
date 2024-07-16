# models.py

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

engine = create_engine('sqlite:///estoque.db', echo=True)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)

class Fornecedor(Base):
    __tablename__ = 'fornecedores'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String) #Permitir CNPJ como opcional

class Material(Base):
    __tablename__ = 'materiais'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    nota_fiscal = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'))
    fornecedor = relationship('Fornecedor')

if __name__ == '__main__':
    Base.metadata.create_all(engine)
