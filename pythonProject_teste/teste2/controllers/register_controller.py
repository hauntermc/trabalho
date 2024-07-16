# controllers/register_controller.py

from utils.encryption_utils import hash_password
from models import Usuario
from utils.db_utils import Session


def register_user(nome, username, password, confirm_password):
    try:
        if password != confirm_password:
            return False, "As senhas não coincidem"

        hashed_password = hash_password(password)

        session = Session()
        novo_usuario = Usuario(nome=nome, username=username, senha=hashed_password)
        session.add(novo_usuario)
        session.commit()
        session.close()

        return True, "Usuário registrado com sucesso"
    except Exception as e:
        print(f"Erro ao registrar usuário: {str(e)}")
        return False, "Erro ao registrar usuário. Verifique os dados e tente novamente"
