from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from sqlalchemy_backend import register_user


class RegisterWindow(QDialog):
    register_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Registrar')
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

        if not username or not password:
            QMessageBox.warning(self, 'Erro de registro', 'Por favor, preencha todos os campos.')
            return
        if password != confirm_password:
            QMessageBox.warning(self, 'Erro de registro', 'As senhas não coincidem.')
            return

        try:
            register_user(username, password, confirm_password)
            self.register_signal.emit(username)
            QMessageBox.information(self, 'Registro', f'Usuário "{username}" registrado com sucesso!')
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, 'Erro de Registro', str(e))
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro inesperado: {str(e)}')

    def cancel_register(self):
        self.reject()
