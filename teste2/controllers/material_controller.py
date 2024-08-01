from models import Material, Fornecedor
from utils.db_utils import Session
from datetime import datetime

def register_material(nome, preco, nota_fiscal, quantidade, fornecedor_nome, data, patrimonio):
    session = None
    try:
        session = Session()

        # Verifica se o fornecedor existe; se não, cria um novo
        fornecedor = session.query(Fornecedor).filter_by(nome=fornecedor_nome).first()
        if not fornecedor:
            fornecedor = Fornecedor(nome=fornecedor_nome, cnpj=None)
            session.add(fornecedor)
            session.commit()  # Comita a adição do fornecedor

        # Verifica se o material com o mesmo patrimônio já existe (se patrimônio fornecido)
        if patrimonio:
            material_existente_patrimonio = session.query(Material).filter_by(patrimonio=patrimonio).first()
            if material_existente_patrimonio:
                print(f"Erro: Patrimônio '{patrimonio}' já está registrado.")
                return False

        # Verifica se o material com a mesma nota fiscal já existe
        material_existente_nota_fiscal = session.query(Material).filter_by(nota_fiscal=nota_fiscal).first()
        if material_existente_nota_fiscal:
            print(f"Erro: Nota fiscal '{nota_fiscal}' já está registrada.")
            return False

        # Adiciona um novo material
        novo_material = Material(
            nome=nome,
            preco=preco,
            nota_fiscal=nota_fiscal,
            quantidade=quantidade,
            data=data,
            fornecedor=fornecedor,
            patrimonio=patrimonio
        )
        session.add(novo_material)
        session.commit()  # Comita a adição do novo material
        print(f"Material '{nome}' registrado com sucesso.")

        return True
    except Exception as e:
        if session:
            session.rollback()  # Rollback da transação em caso de erro
        print(f"Erro ao registrar material: {str(e)}")
        return False
    finally:
        if session:
            session.close()

def is_patrimonio_unique(patrimonio):
    session = None
    try:
        session = Session()
        material = session.query(Material).filter_by(patrimonio=patrimonio).first()
        return material is None
    except Exception as e:
        print(f"Erro ao verificar patrimônio: {str(e)}")
        return False
    finally:
        if session:
            session.close()

def is_nota_fiscal_unique(nota_fiscal):
    session = None
    try:
        session = Session()
        material = session.query(Material).filter_by(nota_fiscal=nota_fiscal).first()
        return material is None
    except Exception as e:
        print(f"Erro ao verificar nota fiscal: {str(e)}")
        return False
    finally:
        if session:
            session.close()
