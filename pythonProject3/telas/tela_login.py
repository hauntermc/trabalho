from PyQt5 import QtWidgets
import bcrypt
from banco_de_dados import session, Usuario

class TelaLogin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 300, 150)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.username_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        login_button = QtWidgets.QPushButton('Login')
        login_button.clicked.connect(self.check_login)

        layout.addWidget(QtWidgets.QLabel('Username:'))
        layout.addWidget(self.username_input)
        layout.addWidget(QtWidgets.QLabel('Password:'))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Buscar o usuário no banco de dados
        user = session.query(Usuario).filter_by(username=username).first()

        if user and self.verify_password(password, user.senha):
            self.accept()  # Permite o login
        else:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'Credenciais inválidas!')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        # Verificar a senha fornecida com o hash armazenado
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
