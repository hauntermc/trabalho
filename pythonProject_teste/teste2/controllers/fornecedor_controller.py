# controllers/fornecedor_controller.py

from models import Fornecedor
from utils.db_utils import Session

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

