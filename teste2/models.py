from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
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
    cnpj = Column(String)  # Permitir CNPJ como opcional
    materiais = relationship('Material', back_populates='fornecedor', cascade="all, delete")

class Material(Base):
    __tablename__ = 'materiais'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    nota_fiscal = Column(String, nullable=False, unique=True)  # Nota fiscal deve ser única
    quantidade = Column(Integer, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'))
    fornecedor = relationship('Fornecedor', back_populates='materiais')

class Tecnico(Base):
    __tablename__ = 'tecnicos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('matricula', name='_matricula_uc'),)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
