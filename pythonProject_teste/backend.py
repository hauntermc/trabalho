# backend.py
from sqlalchemy_backend import register_user, login_user

class Backend:
    def register_user(self, username, password, confirm_password):
        register_user(username, password, confirm_password)

    def login_user(self, username, password):
        return login_user(username, password)
