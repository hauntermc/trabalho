from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from controllers.register_controller import register_user

class RegisterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label_nome = QLabel('Nome')
        self.nome_input = QLineEdit(self)
        layout.addWidget(label_nome)
        layout.addWidget(self.nome_input)

        label_username = QLabel('Username')
        self.username_input = QLineEdit(self)
        layout.addWidget(label_username)
        layout.addWidget(self.username_input)

        label_password = QLabel('Password')
        self.password_input = QLineEdit(self)
        layout.addWidget(label_password)
        layout.addWidget(self.password_input)

        label_confirm_password = QLabel('Confirmar Password')
        self.confirm_password_input = QLineEdit(self)
        layout.addWidget(label_confirm_password)
        layout.addWidget(self.confirm_password_input)

        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def register(self):
        try:
            nome = self.nome_input.text()
            username = self.username_input.text()
            password = self.password_input.text()
            confirm_password = self.confirm_password_input.text()

            success, message = register_user(nome, username, password, confirm_password)
            self.status_label.setText(message)
            if success:
                self.parent().setCurrentIndex(0)
        except Exception as e:
            self.status_label.setText(f"Erro ao registrar: {str(e)}")
