from models import Tecnico
from utils.db_utils import Session

def register_tecnico(nome, telefone, matricula):
    session = Session()

    try:
        # Verifica se a matrícula já está em uso
        if session.query(Tecnico).filter_by(matricula=matricula).first():
            raise ValueError(f"A matrícula '{matricula}' já está em uso.")

        # Cria uma nova instância de Tecnico com os dados fornecidos
        novo_tecnico = Tecnico(nome=nome, telefone=telefone, matricula=matricula)

        # Adiciona o novo técnico à sessão
        session.add(novo_tecnico)

        # Commit para persistir as mudanças no banco de dados
        session.commit()
        return True  # Registro bem-sucedido

    except Exception as e:
        session.rollback()
        print(f"Erro ao registrar técnico: {e}")
        return None  # Outro erro

    finally:
        session.close()

