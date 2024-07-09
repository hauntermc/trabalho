from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QAction, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt

from main_window_button import MainWindowButtons
from register_product_window import RegisterProductWindow
from register_tecnico_window import RegisterTecnicoWindow
from register_fornecedores_window import RegisterFornecedorWindow

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.initUI(username)

    def initUI(self, username):
        label = QLabel(f'Bem-Vindo, {username}!', self)
        label.setAlignment(Qt.AlignCenter)  # Centraliza o texto horizontalmente
        label.setStyleSheet('font-size: 24px;')  # Define o tamanho da fonte

        layout = QVBoxLayout()
        layout.addWidget(label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Configura a barra de menu
        self.menu_bar()

        self.setGeometry(0, 0, 800, 600)
        self.center()

    def center(self):
        # Centraliza a janela na tela
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def menu_bar(self):
        button_actions = MainWindowButtons(self)

        register_produto_action = QAction('Registrar Produto', self)
        register_produto_action.triggered.connect(self.open_register_product_window)
        self.menuBar().addAction(register_produto_action)

        register_tecnico_action = QAction('Registrar Técnico', self)
        register_tecnico_action.triggered.connect(self.open_register_tecnico_window)
        self.menuBar().addAction(register_tecnico_action)

        register_fornecedor_action = QAction('Registrar Fornecedor(a)', self)
        if register_fornecedor_action is not None:
            register_fornecedor_action.triggered.connect(self.open_register_fornecedor_window)
        self.menuBar().addAction(register_fornecedor_action)

        logout_action = QAction('Logout', self)
        logout_action.triggered.connect(self.logout)
        self.menuBar().addAction(logout_action)

    def open_register_tecnico_window(self):
        register_tecnico_window = RegisterTecnicoWindow()
        register_tecnico_window.exec_()

    def open_register_product_window(self):
        register_product_window = RegisterProductWindow()
        register_product_window.exec_()

    def open_register_fornecedor_window(self):
        register_fornecedor_window = RegisterFornecedorWindow()
        register_fornecedor_window.exec_()

    def logout(self):
        self.close()
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()

