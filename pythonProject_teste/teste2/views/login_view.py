from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton
from controllers.login_controller import login_user

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Username')
        layout.addWidget(self.username)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        username = self.username.text()
        password = self.password.text()
        if login_user(username, password):
            print('Login successful')
            self.parent_widget.setCurrentIndex(1)
        else:
            print('Invalid credentials')

    def register(self):
        self.parent_widget.setCurrentIndex(2)
