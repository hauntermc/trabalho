# tecnico_database.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Tecnico(Base):
    __tablename__ = 'tecnicos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    matricula = Column(String, nullable=False)

# Conecta ao banco de dados
engine = create_engine('sqlite:///tecnicos.db')
Base.metadata.create_all(engine)
