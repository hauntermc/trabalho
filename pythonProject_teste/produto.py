# produto.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from estoque_database import Base, Produto, Estoque

# Conecta ao banco de dados
engine_estoque = create_engine('sqlite:///estoque_database.db')
Base.metadata.create_all(engine_estoque)

# Cria uma sessão
Session = sessionmaker(bind=engine_estoque)
session = Session()

def registrar_produto(nome, preco, quantidade_inicial):
    try:
        # Cria e adiciona o novo produto
        novo_produto = Produto(nome=nome, preco=preco)
        session.add(novo_produto)
        session.commit()  # Commit para garantir que o produto tenha um ID

        # Adiciona o produto ao estoque
        novo_estoque = Estoque(produto_id=novo_produto.id, quantidade=quantidade_inicial)
        session.add(novo_estoque)
        session.commit()

        print(f"Produto {nome} registrado com sucesso com quantidade inicial {quantidade_inicial}!")

    except Exception as e:
        print(f"Erro ao registrar produto: {e}")
        session.rollback()

    finally:
        session.close()