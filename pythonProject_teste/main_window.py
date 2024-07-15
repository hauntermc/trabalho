from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QAction, QApplication, QDesktopWidget, \
    QPushButton, QMessageBox, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

from main_window_button import MainWindowButtons
from register_product_window import RegisterProductWindow
from register_tecnico_window import RegisterTecnicoWindow
from register_fornecedores_window import RegisterFornecedorWindow
from print_handler import PrintHandler
from show_tecnico_window import ShowTecnicoWindow
from show_products_window import ShowProductsWindow
from show_fornecedor_window import ShowFornecedores
from saida_material_window import SaidaMaterialWindowDialog
class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.initUI(username)

    def initUI(self, username):
        # Saudação ao usuário
        label = QLabel(f'Bem-Vindo, {username}!', self)
        label.setAlignment(Qt.AlignCenter)  # Centraliza o texto horizontalmente
        label.setStyleSheet('font-size: 24px;')  # Define o tamanho da fonte

        layout = QVBoxLayout()
        layout.addWidget(label)

        # Botões para abrir as janelas de registro
        button_actions = MainWindowButtons(self)

        register_produto_button = QPushButton('Registrar Produto')
        register_produto_button.clicked.connect(self.open_register_product_window)
        layout.addWidget(register_produto_button)

        register_tecnico_button = QPushButton('Registrar Técnico')
        register_tecnico_button.clicked.connect(self.open_register_tecnico_window)
        layout.addWidget(register_tecnico_button)

        register_fornecedor_button = QPushButton('Registrar Fornecedor(a)')
        register_fornecedor_button.clicked.connect(self.open_register_fornecedor_window)
        layout.addWidget(register_fornecedor_button)

        show_products_button = QPushButton('Mostrar Produtos Registrados')
        show_products_button.clicked.connect(self.show_products)
        layout.addWidget(show_products_button)

        show_tecnico_button = QPushButton('Mostrar Técnicos Registrados')
        show_tecnico_button.clicked.connect(self.show_tecnico)
        layout.addWidget(show_tecnico_button)

        show_fornecedor_button = QPushButton('Mostrar Fornecedores Registradors')
        show_fornecedor_button.clicked.connect(self.show_fornecedor)
        layout.addWidget(show_fornecedor_button)

        # Botão para abrir a janela de saída de material
        saida_material_button = QPushButton('Registrar Saída de Material')
        saida_material_button.clicked.connect(self.open_saida_material_window)
        layout.addWidget(saida_material_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Menu de ações
        menu_bar = self.menuBar()

        # Ação de menu para imprimir
        print_action = QAction('Imprimir', self)
        print_action.triggered.connect(self.print_report)
        menu_bar.addAction(print_action)

        # Adicionar widget vazio para empurrar o botão de logout para a direita
        empty_widget = QWidget(self)
        empty_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        menu_bar.setCornerWidget(empty_widget, Qt.TopLeftCorner)

        # Botão de logout na barra de menu
        logout_button = QPushButton('Logout', self)
        logout_button.clicked.connect(self.confirm_logout)
        logout_button.setStyleSheet('padding: 5px 10px;')  # Customize a aparência do botão se necessário
        menu_bar.setCornerWidget(logout_button, Qt.TopRightCorner)

        self.setGeometry(0, 0, 800, 600)
        self.center()

    def confirm_logout(self):
        # Exibe uma mensagem de confirmação para o logout
        reply = QMessageBox.question(self, 'Confirmar Logout', 'Tem certeza que quer deslogar?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.logout()

    def logout(self):
        # Fecha a janela atual e abre a janela de login
        self.close()
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()

    def center(self):
        # Centraliza a janela na tela
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_register_tecnico_window(self):
        try:
            register_tecnico_window = RegisterTecnicoWindow()
            register_tecnico_window.exec_()
        except Exception as e:
            print(f'Erro ao abrir janela de registro de técnico: {e}')

    def open_register_product_window(self):
        try:
            register_product_window = RegisterProductWindow()
            register_product_window.exec_()
        except Exception as e:
            print(f'Erro ao abrir janela de registro de produto: {e}')

    def open_register_fornecedor_window(self):
        try:
            register_fornecedor_window = RegisterFornecedorWindow()
            register_fornecedor_window.exec_()
        except Exception as e:
            print(f'Erro ao abrir janela de registro de fornecedor: {e}')

    def print_report(self):
        print_handler = PrintHandler(self)
        print_handler.print_report()

    def show_products(self):
        try:
            show_products_window = ShowProductsWindow()
            show_products_window.exec_()
        except Exception as e:
            QMessageBox.warning(self, f'{e}')

    def show_tecnico(self):
        try:
            show_tecnico_window = ShowTecnicoWindow()
            show_tecnico_window.exec_()
        except Exception as e:
            QMessageBox.warning(self, f'{e}')

    def show_fornecedor(self):
        try:
            show_fornecedor_window = ShowFornecedores()
            show_fornecedor_window.exec_()
        except Exception as e:
            error_message = f'Ocorreu um erro ao abrir a janela de fornecedores:\n\n{str(e)}'
            QMessageBox.critical(self, 'Erro', error_message)

    def open_saida_material_window(self):
        try:
            saida_material_window = SaidaMaterialWindowDialog()
            saida_material_window.exec_()
        except Exception as e:
            print(f'Erro ao abrir janela de saída de material: {e}')