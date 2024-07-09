from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt

engine = create_engine('sqlite:///usuarios.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)

    def __repr__(self):
        return f"<Usuario(username='{self.username}')>"

Base.metadata.create_all(engine)

def register_user(username, password, confirm_password):
    if password != confirm_password:
        raise ValueError("Senhas não coincidem.")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    session = Session()
    try:
        existing_user = session.query(Usuario).filter_by(username=username).first()
        if existing_user:
            raise ValueError(f"Usuário '{username}' já existe.")

        new_user = Usuario(username=username, password_hash=hashed_password.decode('utf-8'))
        session.add(new_user)
        session.commit()
        print(f"Usuário '{username}' registrado com sucesso!")
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def login_user(username, password):
    session = Session()
    try:
        user = session.query(Usuario).filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
