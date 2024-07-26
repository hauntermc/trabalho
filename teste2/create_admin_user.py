from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Usuario
from utils.encryption_utils import hash_password

# Configuração do banco de dados
engine = create_engine('sqlite:///estoque.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def create_admin_user():
    # Verificar se o usuário admin já existe
    admin_user = session.query(Usuario).filter_by(username='admin').first()
    if not admin_user:
        # Criar um novo usuário admin
        hashed_password = hash_password('admin')  # Criptografar a senha
        admin_user = Usuario(nome='Admin', username='admin', senha=hashed_password)
        session.add(admin_user)
        session.commit()
        print("Usuário admin criado com sucesso.")
    else:
        print("Usuário admin já existe.")

if __name__ == '__main__':
    create_admin_user()