from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Material, RetornoMaterial, RetiradaMaterial, Fornecedor,Tecnico

# Configuração do banco de dados
engine = create_engine('sqlite:///estoque.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def clear_products_table():
    try:
        # Excluir todos os registros da tabela 'materiais'
        session.query(RetornoMaterial).delete()
        session.query(Tecnico).delete()
        session.query(Fornecedor).delete()
        session.query(RetiradaMaterial).delete()
        session.query(Material).delete()
        # Confirmar a transação
        session.commit()
        print("Tabela 'materiais' limpa com sucesso.")
    except Exception as e:
        # Em caso de erro, fazer rollback da transação
        session.rollback()
        print(f"Erro ao limpar a tabela 'materiais': {e}")
    finally:
        # Fechar a sessão
        session.close()

if __name__ == '__main__':
    clear_products_table()
