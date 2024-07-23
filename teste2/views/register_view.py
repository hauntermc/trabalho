from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Usuario  # Certifique-se de que 'models' é o nome do seu arquivo de modelos e 'Usuario' é o nome da classe


class RegisterWindow(QWidget):
    # Sinal personalizado para indicar que a janela foi fechada
    register_window_closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Registro de Usuário')
        self.setGeometry(100, 100, 300, 200)

        self.username_label = QLabel('Username:', self)
        self.username_input = QLineEdit(self)

        self.password_label = QLabel('Password:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_label = QLabel('Confirm Password:', self)
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton('Register', self)
        self.cancel_button = QPushButton('Cancel', self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.confirm_password_label)
        self.layout.addWidget(self.confirm_password_input)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.cancel_button)

        self.register_button.clicked.connect(self.register)
        self.cancel_button.clicked.connect(self.close)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password or not confirm_password:
            self.show_message("Erro", "Todos os campos devem ser preenchidos.")
            return

        if password != confirm_password:
            self.show_message("Erro", "As senhas não coincidem.")
            return

        # Aqui você pode adicionar a lógica para salvar o usuário no banco de dados
        try:
            engine = create_engine('sqlite:///usuarios.db')
            Session = sessionmaker(bind=engine)
            session = Session()

            # Verifica se o nome de usuário já existe
            if session.query(Usuario).filter_by(username=username).first():
                self.show_message("Erro", "Nome de usuário já existe.")
                return

            # Adiciona o novo usuário
            new_user = Usuario(username=username, senha=password)
            session.add(new_user)
            session.commit()
            session.close()

            self.show_message("Sucesso", "Usuário registrado com sucesso.")
            self.close()
        except Exception as e:
            self.show_message("Erro", f"Erro ao registrar usuário: {e}")

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def closeEvent(self, event):
        self.register_window_closed.emit()  # Emite o sinal personalizado quando a janela é fechada
        super().closeEvent(event)
