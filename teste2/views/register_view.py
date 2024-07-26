from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Usuario  # Certifique-se de que 'models' é o nome do seu arquivo de modelos e 'Usuario' é o nome da classe

class RegisterWindow(QWidget):
    # Sinal personalizado para indicar que a janela foi fechada
    register_window_closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Registro de Usuário')
        self.setGeometry(100, 100, 400, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)

        # Título
        title_label = QLabel('Registro de Usuário')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 18, QFont.Bold))
        title_label.setStyleSheet("color: #333;")
        layout.addWidget(title_label)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Campo de nome de usuário
        username_label = QLabel('Nome de Usuário:', self)
        username_label.setFont(QFont('Arial', 12))
        username_label.setStyleSheet("color: #555;")
        self.username_input = QLineEdit(self)
        self.username_input.setFont(QFont('Arial', 12))
        self.username_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.username_input.setStyleSheet("background-color: #FAFAFA; border: 1px solid #DDDDDD; border-radius: 5px; padding: 10px;")
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Campo de senha
        password_label = QLabel('Senha:', self)
        password_label.setFont(QFont('Arial', 12))
        password_label.setStyleSheet("color: #555;")
        self.password_input = QLineEdit(self)
        self.password_input.setFont(QFont('Arial', 12))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.password_input.setStyleSheet("background-color: #FAFAFA; border: 1px solid #DDDDDD; border-radius: 5px; padding: 10px;")
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Campo de confirmação de senha
        confirm_password_label = QLabel('Confirmar Senha:', self)
        confirm_password_label.setFont(QFont('Arial', 12))
        confirm_password_label.setStyleSheet("color: #555;")
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setFont(QFont('Arial', 12))
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.confirm_password_input.setStyleSheet("background-color: #FAFAFA; border: 1px solid #DDDDDD; border-radius: 5px; padding: 10px;")
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_input)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botões de Registrar e Cancelar
        self.register_button = QPushButton('Registrar', self)
        self.register_button.setFont(QFont('Arial', 14))
        self.register_button.setStyleSheet("background-color: #28A745; color: white; border-radius: 5px; padding: 10px 20px;")
        self.register_button.clicked.connect(self.register)
        self.register_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(self.register_button)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.cancel_button = QPushButton('Cancelar', self)
        self.cancel_button.setFont(QFont('Arial', 14))
        self.cancel_button.setStyleSheet("background-color: #DC3545; color: white; border-radius: 5px; padding: 10px 20px;")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(self.cancel_button)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

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
