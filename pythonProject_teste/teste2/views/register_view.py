# views/register_view.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from controllers.register_controller import register_user

class RegisterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.nome = QLineEdit(self)
        self.nome.setPlaceholderText('Nome')
        layout.addWidget(self.nome)

        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Username')
        layout.addWidget(self.username)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.confirm_password = QLineEdit(self)
        self.confirm_password.setPlaceholderText('Confirm Password')
        self.confirm_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password)

        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def register(self):
        nome = self.nome.text()
        username = self.username.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()

        success, message = register_user(nome, username, password, confirm_password)
        self.status_label.setText(message)
        if success:
            self.parent().setCurrentIndex(0)
