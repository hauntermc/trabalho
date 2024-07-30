import sys
from PyQt5.QtWidgets import (QApplication, QStackedWidget, QDialog, QVBoxLayout,
                             QLineEdit, QPushButton, QMessageBox, QWidget, QDesktopWidget, QFileDialog)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

from utils.pdf_utils import generate_form_pdf
from views.login_view import LoginWindow
from views.after_login_view import AfterLoginScreen
from views.material_registration_view import MaterialRegistrationWindow
from views.fornecedor_registration_view import FornecedorRegistrationWindow
from views.showWithDraw_window import ShowWithdrawalsWindow
from views.tecnico_registration_view import TecnicoRegistrationWindow
from views.showproducts_window import ShowProductsWindow
from views.showtecnico_view import ShowTecnicoWindow
from views.material_withdraw_window import MaterialWithdrawWindow
from views.retorno_material_view import RetornoMaterialWindow
from views.show_estoque_total import ShowStockWindow
from views.user_registration_view import UserRegistrationWindow
from utils.db_utils import Session

import logging

# Configura o logging
logging.basicConfig(level=logging.WARNING)  # Define o nível de logging para WARNING
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.WARNING)  # Define o nível

class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Autenticação')
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f4f8;  /* Azul claro */
                font-family: Arial, sans-serif;
            }
            QLineEdit {
                border: 1px solid #007acc;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                background-color: #ffffff;
                min-width: 200px;  # Define a largura mínima
                max-width: 200px;  # Define a largura máxima
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)

        layout = QVBoxLayout()
        self.password_line_edit = QLineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_line_edit)

        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def get_password(self):
        return self.password_line_edit.text()


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Controle de Materiais")
        self.setStyleSheet("""
            QStackedWidget {
                background-color: #f0f4f8;  /* Azul claro */
                font-family: Arial, sans-serif;
            }
            QLineEdit {
                min-width: 200px;  # Define a largura mínima
                max-width: 200px;  # Define a largura máxima
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)

        self.login_window = LoginWindow(self)
        self.after_login_screen = AfterLoginScreen()
        self.addWidget(self.login_window)
        self.addWidget(self.after_login_screen)

        # Conectar os botões usando o dicionário all_buttons
        self.after_login_screen.all_buttons['Registrar Produto'].clicked.connect(
            lambda: self.abrir_janela('material_registration', MaterialRegistrationWindow))
        self.after_login_screen.all_buttons['Registrar Fornecedor'].clicked.connect(
            lambda: self.abrir_janela('fornecedor_registration', FornecedorRegistrationWindow))
        self.after_login_screen.all_buttons['Registrar Técnico'].clicked.connect(
            lambda: self.abrir_janela('tecnico_registration', TecnicoRegistrationWindow))
        self.after_login_screen.all_buttons['Retirar Material'].clicked.connect(
            lambda: self.abrir_janela('material_withdraw', MaterialWithdrawWindow))
        self.after_login_screen.all_buttons['Retorno de Material'].clicked.connect(
            lambda: self.abrir_janela('retorno_material', RetornoMaterialWindow))
        self.after_login_screen.all_buttons['Mostrar Produtos'].clicked.connect(
            lambda: self.abrir_janela('show_products', ShowProductsWindow))
        self.after_login_screen.all_buttons['Mostrar Técnicos'].clicked.connect(
            lambda: self.abrir_janela('show_tecnico', ShowTecnicoWindow))
        self.after_login_screen.all_buttons['Mostrar Produtos Retirados'].clicked.connect(
            lambda: self.abrir_janela('show_withdrawals', ShowWithdrawalsWindow))
        self.after_login_screen.all_buttons['Mostrar Estoque Total'].clicked.connect(
            lambda: self.abrir_janela('show_estoque', ShowStockWindow))
        self.after_login_screen.all_buttons['Adicionar Novo Usuário'].clicked.connect(self.abrir_tela_registro_usuario)
        self.after_login_screen.btn_logout.clicked.connect(self.confirm_logout)

        self.windows = {
            'material_registration': None,
            'fornecedor_registration': None,
            'tecnico_registration': None,
            'show_products': None,
            'show_tecnico': None,
            'material_withdraw': None,
            'retorno_material': None,
            'show_withdrawals': None,
            'show_estoque': None,
            'user_registration': None
        }

        self.setCurrentIndex(0)

    def abrir_tela_registro_usuario(self):
        dialog = PasswordDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            password = dialog.get_password()
            if password == 'admin':
                self.abrir_janela('user_registration', UserRegistrationWindow)
            else:
                QMessageBox.warning(self, 'Acesso Negado', 'Senha administrativa incorreta!')

    def abrir_janela(self, janela_key, janela_class):
        try:
            if not self.windows[janela_key]:
                self.windows[janela_key] = janela_class()
            if not self.windows[janela_key].isVisible():
                self.windows[janela_key].show()
            logging.info(f"Janela '{janela_key}' aberta com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao abrir a janela '{janela_key}': {e}")

    def confirm_logout(self):
        reply = QMessageBox.question(self, 'Confirmação',
                                     'Você realmente deseja fazer logout?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.logout()

    def logout(self):
        logging.info("Usuário realizando logout.")
        self.fechar_todas_as_janelas()
        self.setCurrentIndex(0)

    def closeEvent(self, event):
        logging.info("Aplicativo fechado. Fechando todas as janelas.")
        self.fechar_todas_as_janelas()
        reply = QMessageBox.question(self, 'Confirmação',
                                     'Você realmente deseja sair?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            logging.info("Usuário confirmou a saída. Realizando logout.")
            self.logout()
            event.accept()
        else:
            logging.info("Usuário cancelou a saída.")
            event.ignore()

    def fechar_todas_as_janelas(self):
        for window in self.windows.values():
            if window:
                window.close()

    def update_products(self):
        # Atualizar o QComboBox de produtos
        self.material_withdraw_window.update_products()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # Ajusta o tamanho da janela para cobrir toda a tela
    screen_rect = QDesktopWidget().availableGeometry()
    window.setGeometry(screen_rect)

    window.show()  # Exibe a janela principal
    sys.exit(app.exec_())
