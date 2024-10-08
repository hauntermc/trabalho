from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint, Date, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# Configuração do banco de dados
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
    nome = Column(String, nullable=False)  # Garantir unicidade do nome
    preco = Column(Float, nullable=False)
    nota_fiscal = Column(String, nullable=True)  # Nota fiscal opcional
    quantidade = Column(Integer, nullable=False)  # Permite valores zero
    data = Column(DateTime, default=datetime.utcnow)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'))
    fornecedor = relationship('Fornecedor', back_populates='materiais')
    retiradas = relationship('RetiradaMaterial', back_populates='produto')
    retornos = relationship('RetornoMaterial', back_populates='produto')
    patrimonio = Column(String, nullable=True)  # Permitir patrimônio nulo
    estoque_minimo = Column(Integer, nullable=False)

class Tecnico(Base):
    __tablename__ = 'tecnicos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=False)
    retiradas = relationship('RetiradaMaterial', back_populates='tecnico')
    retornos = relationship('RetornoMaterial', back_populates='tecnico')

    __table_args__ = (UniqueConstraint('matricula', name='_matricula_uc'),)

class RetiradaMaterial(Base):
    __tablename__ = 'retirada_material'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True, nullable=False)
    ordem_servico = Column(String(50), unique=True, nullable=False)
    produto_id = Column(Integer, ForeignKey('materiais.id'), nullable=False)
    tecnico_id = Column(Integer, ForeignKey('tecnicos.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data = Column(Date, nullable=False)
    local = Column(Text, nullable=False)
    devolvido = Column(Boolean, default=False)  # Campo para indicar se o material foi devolvido
    patrimonio = Column(String)

    produto = relationship('Material', back_populates='retiradas')
    tecnico = relationship('Tecnico', back_populates='retiradas')

    def __repr__(self):
        devolvido_str = "Sim" if self.devolvido else "Não"
        return (f"<RetiradaMaterial(codigo={self.codigo}, ordem_servico={self.ordem_servico}, "
                f"produto_id={self.produto_id}, tecnico_id={self.tecnico_id}, quantidade={self.quantidade}, "
                f"data={self.data}, local={self.local}, devolvido={devolvido_str})>")

class RetornoMaterial(Base):
    __tablename__ = 'retorno_material'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ordem_servico = Column(String(50), nullable=False)
    produto_id = Column(Integer, ForeignKey('materiais.id'), nullable=False)
    tecnico_id = Column(Integer, ForeignKey('tecnicos.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_retorno = Column(DateTime, default=datetime.utcnow, nullable=False)
    data = Column(Date, nullable=False)

    produto = relationship('Material', back_populates='retornos')
    tecnico = relationship('Tecnico', back_populates='retornos')

    def __repr__(self):
        return (f"<RetornoMaterial(ordem_servico={self.ordem_servico}, produto_id={self.produto_id}, "
                f"tecnico_id={self.tecnico_id}, quantidade={self.quantidade}, data_retorno={self.data_retorno}, "
                f"data={self.data})>")

if __name__ == '__main__':
    Base.metadata.create_all(engine)
