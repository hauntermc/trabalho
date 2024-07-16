from utils.db_utils import session
from models import Usuario
from utils.encryption_utils import check_password

def login_user(username, password):
    user = session.query(Usuario).filter_by(username=username).first()
    if user and check_password(user.senha, password):
        return True
    return False