from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from utils.db_utils import session
from models import Usuario
from utils.encryption_utils import hash_password

class UserRegistrationWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Configurar estilo
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;  /* Azul claro */
                color: #333;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #007acc;  /* Azul mais escuro */
            }
            QLineEdit {
                border: 1px solid #007acc;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)

        # Nome do usuário
        label_usuario = QLabel('Nome do Usuário')
        self.username_input = QLineEdit(self)
        layout.addWidget(label_usuario)
        layout.addWidget(self.username_input)

        # Senha
        label_senha = QLabel('Senha')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Ocultar senha
        layout.addWidget(label_senha)
        layout.addWidget(self.password_input)

        # Confirmar senha
        label_confirm_senha = QLabel('Confirmar Senha')
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)  # Ocultar senha
        layout.addWidget(label_confirm_senha)
        layout.addWidget(self.confirm_password_input)

        # Botão de registro
        self.register_button = QPushButton('Registrar', self)
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)

        self.setLayout(layout)
        self.setWindowTitle('Registrar Novo Usuário')

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos!')
            return

        if password != confirm_password:
            QMessageBox.warning(self, 'Erro', 'As senhas não coincidem!')
            return

        try:
            hashed_password = hash_password(password)
            new_user = Usuario(nome=username, username=username, senha=hashed_password)
            session.add(new_user)
            session.commit()
            QMessageBox.information(self, 'Sucesso', 'Usuário registrado com sucesso!')
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao registrar usuário: {e}')
