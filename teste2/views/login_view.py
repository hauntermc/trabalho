from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QSizePolicy, QSpacerItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QGuiApplication
import qt_material
from controllers.login_controller import login_user
from views.register_view import RegisterWindow

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.register_window = None
        self.initUI()
        qt_material.apply_stylesheet(self, theme='light_blue.xml')
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(400, 300)
        self.center()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Título
        title_label = QLabel('SISTEMA DE CONTROLE DE MATERIAIS')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 36, QFont.Bold))
        title_label.setStyleSheet("color: #333;")
        layout.addWidget(title_label)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Campo de usuário
        label_username = QLabel('Usuário')
        label_username.setFont(QFont('Arial', 14))
        label_username.setStyleSheet("color: #555;")
        self.username_input = QLineEdit(self)
        self.username_input.setFont(QFont('Arial', 14))
        self.username_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.username_input.setStyleSheet("background-color: #FAFAFA; border: 1px solid #DDDDDD; border-radius: 8px; padding: 5px;")
        layout.addWidget(label_username)
        layout.addWidget(self.username_input)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Campo de senha
        label_password = QLabel('Senha')
        label_password.setFont(QFont('Arial', 14))
        label_password.setStyleSheet("color: #555;")
        self.password_input = QLineEdit(self)
        self.password_input.setFont(QFont('Arial', 14))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.password_input.setStyleSheet("background-color: #FAFAFA; border: 1px solid #DDDDDD; border-radius: 8px; padding: 5px;")
        layout.addWidget(label_password)
        layout.addWidget(self.password_input)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botões de Login e Register
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        self.login_button = QPushButton('Login', self)
        self.login_button.setFont(QFont('Arial', 14))
        self.login_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 8px; padding: 10px;")
        self.login_button.clicked.connect(self.login)
        self.login_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        buttons_layout.addWidget(self.login_button)

        self.register_button = QPushButton('Registrar', self)
        self.register_button.setFont(QFont('Arial', 14))
        self.register_button.setStyleSheet("background-color: #28A745; color: white; border-radius: 8px; padding: 10px;")
        self.register_button.clicked.connect(self.register)
        self.register_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        buttons_layout.addWidget(self.register_button)

        layout.addLayout(buttons_layout)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if login_user(username, password):
            self.parent_widget.setCurrentIndex(1)
        else:
            self.show_error_message("Usuário ou senha incorretos.")

    def register(self):
        try:
            if self.register_window is None or not self.register_window.isVisible():
                if self.register_window is None:
                    self.register_window = RegisterWindow(self)
                    self.register_window.destroyed.connect(self.on_register_window_closed)
                self.register_window.show()
        except Exception as e:
            self.show_error_message(f"Erro ao abrir a tela de registro: {e}")

    def on_register_window_closed(self):
        self.register_window = None

    def show_error_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle('Erro')
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def center(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        widget_geometry = self.geometry()
        widget_geometry.moveCenter(screen_geometry.center())
        self.setGeometry(widget_geometry)
