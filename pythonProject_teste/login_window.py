# login_window.py
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSlot
from database import Database
from register_window import RegisterWindow

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.backend = Database()  # Instância do banco de dados
        self.initUI()

    def initUI(self):
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton('Login')
        register_button = QPushButton('Registrar')

        vbox = QVBoxLayout()
        vbox.addWidget(self.username_input)
        vbox.addWidget(self.password_input)
        vbox.addWidget(login_button)
        vbox.addWidget(register_button)

        self.setLayout(vbox)

        login_button.clicked.connect(self.login)
        register_button.clicked.connect(self.open_register_window)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.backend.login_user(username, password):
            QMessageBox.information(self, 'Login', 'Login bem-sucedido!')
            self.accept()  # Fecha a janela de login
        else:
            QMessageBox.warning(self, 'Erro de Login', 'Usuário ou senha incorretos.')

    def open_register_window(self):
        self.hide()  # Esconde a janela de login
        register_window = RegisterWindow(self, self.backend)  # Passa o backend para o RegisterWindow
        register_window.register_signal.connect(self.registered)  # Conecta ao slot registered
        register_window.exec_()  # Executa a janela de registro

    @pyqtSlot(str)
    def registered(self, username):
        QMessageBox.information(self, 'Registro', f'Usuário "{username}" registrado com sucesso!')
        self.show()  # Mostra a janela de login após o registro
