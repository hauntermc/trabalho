from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel,
                             QHBoxLayout, QSizePolicy, QSpacerItem, QMessageBox,
                             QGraphicsDropShadowEffect, QFileDialog, QApplication)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QGuiApplication, QColor, QPixmap
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
        self.center()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)

        # Título
        title_label = QLabel('SISTEMA DE CONTROLE DE MATERIAIS')
        title_label.setFont(QFont('Segoe UI', 24, QFont.Bold))  # Tamanho de fonte ajustado
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #333;  /* Cor do texto */
            font-size: 24px; /* Tamanho da fonte */
            padding: 15px;  /* Espaçamento interno */
            font-weight: bold;  /* Negrito */
        """)
        title_label.setGraphicsEffect(self.create_shadow_effect())  # Adiciona sombra ao texto

        layout.addWidget(title_label)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Imagem
        image_label = QLabel(self)
        pixmap = QPixmap('C:/Users/Detel/Desktop/teste2/logo-pjerj-preto.png')  # Substitua pelo caminho da sua imagem
        scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Redimensiona a imagem
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Campo de usuário
        label_username = QLabel('Usuário')
        label_username.setFont(QFont('Arial', 12))
        label_username.setStyleSheet("color: #555;")
        self.username_input = QLineEdit(self)
        self.username_input.setFont(QFont('Arial', 12))
        self.username_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.username_input.setStyleSheet("background-color: #FAFAFA; border: 1px solid #DDDDDD; border-radius: 5px; padding: 10px;")
        self.username_input.setMaximumWidth(300)  # Define largura máxima
        self.username_input.setMinimumWidth(200)  # Define largura mínima
        self.username_input.returnPressed.connect(self.login)  # Conectar Enter ao método de login
        layout.addWidget(label_username, 0, Qt.AlignCenter)  # Centraliza o rótulo
        layout.addWidget(self.username_input, 0, Qt.AlignCenter)  # Centraliza o campo de entrada

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Campo de senha
        label_password = QLabel('Senha')
        label_password.setFont(QFont('Arial', 12))
        label_password.setStyleSheet("color: #555;")
        self.password_input = QLineEdit(self)
        self.password_input.setFont(QFont('Arial', 12))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.password_input.setStyleSheet("background-color: #FAFAFA; border: 1px solid #DDDDDD; border-radius: 5px; padding: 10px;")
        self.password_input.setMaximumWidth(300)  # Define largura máxima
        self.password_input.setMinimumWidth(200)  # Define largura mínima
        self.password_input.returnPressed.connect(self.login)  # Conectar Enter ao método de login
        layout.addWidget(label_password, 0, Qt.AlignCenter)  # Centraliza o rótulo
        layout.addWidget(self.password_input, 0, Qt.AlignCenter)  # Centraliza o campo de entrada

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botões de Login
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.login_button = QPushButton('Login', self)
        self.login_button.setFont(QFont('Arial', 14))
        self.login_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 5px; padding: 10px 20px;")
        self.login_button.setMaximumWidth(150)  # Define largura máxima
        self.login_button.setMinimumWidth(100)  # Define largura mínima
        self.login_button.clicked.connect(self.login)
        self.login_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        buttons_layout.addWidget(self.login_button, 0, Qt.AlignCenter)  # Centraliza o botão

        layout.addLayout(buttons_layout)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

        self.showMaximized()  # Abre a janela maximizada

    def create_shadow_effect(self):
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(10)
        shadow_effect.setOffset(2, 2)
        shadow_effect.setColor(QColor(0, 0, 0, 50))  # Cor da sombra com transparência
        return shadow_effect

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if login_user(username, password):
            self.parent_widget.setCurrentIndex(1)
        else:
            self.show_error_message("Usuário ou senha incorretos.")

    def open_register_window(self):
        if self.register_window is None or not self.register_window.isVisible():
            if self.register_window is None:
                self.register_window = RegisterWindow(self)
                self.register_window.register_window_closed.connect(self.on_register_window_closed)
            self.register_window.show()

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

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
