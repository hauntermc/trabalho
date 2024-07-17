from models import Material, Fornecedor
from utils.db_utils import Session
from datetime import datetime

def register_material(nome, preco, nota_fiscal, quantidade, fornecedor_nome, data):
    session = None
    try:
        session = Session()

        # Verifica se o fornecedor já existe no banco de dados pelo nome
        fornecedor = session.query(Fornecedor).filter_by(nome=fornecedor_nome).first()
        if not fornecedor:
            # Se o fornecedor não existe, registra ele com CNPJ None
            fornecedor = register_fornecedor(fornecedor_nome, cnpj=None)
            if not fornecedor:
                raise Exception(f"Fornecedor '{fornecedor_nome}' não pôde ser registrado.")

        # Cria um novo material associado ao fornecedor
        novo_material = Material(nome=nome, preco=preco, nota_fiscal=nota_fiscal,
                                 quantidade=quantidade, data=data,
                                 fornecedor=fornecedor)

        session.add(novo_material)
        session.commit()

        return True
    except Exception as e:
        session.rollback()  # Rollback da transação em caso de erro
        print(f"Erro ao registrar material: {str(e)}")
        return False
    finally:
        if session:
            session.close()

def register_fornecedor(nome, cnpj=None):
    session = None
    try:
        session = Session()

        # Verifica se o fornecedor já existe no banco de dados pelo nome
        fornecedor = session.query(Fornecedor).filter_by(nome=nome).first()
        if fornecedor:
            print(f"Fornecedor '{nome}' já está registrado.")
            return fornecedor

        # Cria um novo fornecedor
        novo_fornecedor = Fornecedor(nome=nome, cnpj=cnpj)
        session.add(novo_fornecedor)
        session.commit()

        print(f"Fornecedor '{nome}' registrado com sucesso.")
        return novo_fornecedor
    except Exception as e:
        session.rollback()  # Rollback da transação em caso de erro
        print(f"Erro ao registrar fornecedor: {str(e)}")
        return None
    finally:
        if session:
            session.close()
