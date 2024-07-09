from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from sqlalchemy_backend import login_user
from main_window import MainWindow
from register_window import RegisterWindow

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.initUI()

    def initUI(self):
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton('Login')
        register_button = QPushButton('Registrar')

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('Usuário:'))
        vbox.addWidget(self.username_input)
        vbox.addWidget(QLabel('Senha:'))
        vbox.addWidget(self.password_input)
        vbox.addWidget(login_button)
        vbox.addWidget(register_button)

        self.setLayout(vbox)

        login_button.clicked.connect(self.login)
        register_button.clicked.connect(self.open_register_window)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if login_user(username, password):
            self.accept()
            self.main_window = MainWindow(username)
            self.main_window.show()
        else:
            QMessageBox.warning(self, 'Erro de Login', 'Credenciais inválidas.')

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.hide()
        self.register_window.exec_()
        self.show()
