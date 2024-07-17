from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from controllers.login_controller import login_user

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label_username = QLabel('Username')
        self.username_input = QLineEdit(self)
        layout.addWidget(label_username)
        layout.addWidget(self.username_input)

        label_password = QLabel('Password')
        self.password_input = QLineEdit(self)
        layout.addWidget(label_password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton('Register', self)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if login_user(username, password):
            print('Login successful')
            self.parent_widget.setCurrentIndex(1)
        else:
            print('Invalid credentials')

    def register(self):
        self.parent_widget.abrir_tela_register()
