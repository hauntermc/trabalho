from models import Material, Fornecedor
from utils.db_utils import Session
from datetime import datetime

def register_material(nome, preco, nota_fiscal, quantidade, fornecedor_nome, data, patrimonio):
    session = None
    try:
        session = Session()
        fornecedor = session.query(Fornecedor).filter_by(nome=fornecedor_nome).first()
        if not fornecedor:
            fornecedor = Fornecedor(nome=fornecedor_nome, cnpj=None)
            session.add(fornecedor)
            session.commit()

        material_existente = session.query(Material).filter_by(nome=nome, nota_fiscal=nota_fiscal).first()
        if material_existente:
            material_existente.quantidade += quantidade
            session.commit()
            print(f"Quantidade do material '{nome}' atualizada com sucesso.")
        else:
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
            session.commit()
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
