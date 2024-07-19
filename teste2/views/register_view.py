from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QStackedWidget
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
        self.password_input.setEchoMode(QLineEdit.Password)  # Mostra a senha como asteriscos
        layout.addWidget(label_password)
        layout.addWidget(self.password_input)

        label_confirm_password = QLabel('Confirmar Password')
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)  # Mostra a senha como asteriscos
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

            if len(username) < 4:
                self.status_label.setText("Username deve ter pelo menos 4 caracteres.")
                return

            if len(password) < 4:
                self.status_label.setText("Senha deve ter pelo menos 4 caracteres.")
                return

            if password != confirm_password:
                self.status_label.setText("As senhas não correspondem.")
                return

            success, message = register_user(nome, username, password, confirm_password)
            self.status_label.setText(message)
            if success:
                self.nome_input.clear()  # Limpa o campo Nome
                self.username_input.clear()  # Limpa o campo Username
                self.password_input.clear()  # Limpa o campo Password
                self.confirm_password_input.clear()  # Limpa o campo Confirmar Password
                self.status_label.setText("Registrado com sucesso")
                parent_widget = self.parent()
                if parent_widget and isinstance(parent_widget, QStackedWidget):
                    parent_widget.setCurrentIndex(0)
                else:
                    self.status_label.setText("Erro ao registrar: parent_widget é None ou não é um QStackedWidget")
        except Exception as e:
            self.status_label.setText(f"Erro ao registrar: {str(e)}")
