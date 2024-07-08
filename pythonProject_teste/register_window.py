# register_window.py
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox
from database import Database

class RegisterWindow(QDialog):
    register_signal = pyqtSignal(str)  # Sinal para registrar usuário

    def __init__(self, parent=None, backend=None):
        super().__init__(parent)
        self.setWindowTitle('Registrar')
        self.backend = backend if backend else Database()  # Instância do backend
        self.initUI()

    def initUI(self):
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.confirm_password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        register_button = QPushButton('Registrar')
        cancel_button = QPushButton('Cancelar')

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('Usuário:'))
        vbox.addWidget(self.username_input)
        vbox.addWidget(QLabel('Senha:'))
        vbox.addWidget(self.password_input)
        vbox.addWidget(QLabel('Confirmar Senha:'))
        vbox.addWidget(self.confirm_password_input)
        vbox.addWidget(register_button)
        vbox.addWidget(cancel_button)

        self.setLayout(vbox)

        register_button.clicked.connect(self.register)
        cancel_button.clicked.connect(self.cancel_register)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, 'Erro de Registro', 'Por favor, preencha todos os campos.')
            return

        if password != confirm_password:
            QMessageBox.warning(self, 'Erro de Registro', 'As senhas não coincidem.')
            return

        try:
            self.backend.register_user(username, password)
            self.register_signal.emit(username)  # Emitir sinal com o nome de usuário registrado
            QMessageBox.information(self, 'Registro', f'Usuário "{username}" registrado com sucesso!')
            self.close()  # Fecha a janela de registro
        except ValueError as e:
            QMessageBox.warning(self, 'Erro de Registro', str(e))

    def cancel_register(self):
        self.reject()  # Rejeita (fecha) a janela de registro
        parent = self.parent()
        if parent:
            parent.show()  # Mostra a janela de login ao cancelar o registro
