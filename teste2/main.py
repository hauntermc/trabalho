import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from views.login_view import LoginWindow
from views.after_login_view import AfterLoginScreen
from views.material_registration_view import MaterialRegistrationWindow
from views.fornecedor_registration_view import FornecedorRegistrationWindow
from views.showWithDraw_window import ShowWithdrawalsWindow
from views.tecnico_registration_view import TecnicoRegistrationWindow
from views.register_view import RegisterWindow
from views.showproducts_window import ShowProductsWindow
from views.showtecnico_view import ShowTecnicoWindow
from views.material_withdraw_window import MaterialWithdrawWindow
from views.retorno_material_view import RetornoMaterialWindow
from views.show_estoque_total import ShowStockWindow


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.login_window = LoginWindow(self)
        self.after_login_screen = AfterLoginScreen()
        self.register_window = None

        self.addWidget(self.login_window)
        self.addWidget(self.after_login_screen)

        self.after_login_screen.btn_registrar_produto.clicked.connect(self.abrir_tela_registro_produto)
        self.after_login_screen.btn_registrar_fornecedor.clicked.connect(self.abrir_tela_registro_fornecedor)
        self.after_login_screen.btn_registrar_tecnico.clicked.connect(self.abrir_tela_registro_tecnico)
        self.after_login_screen.btn_retirar_material.clicked.connect(self.abrir_janela_retirar_material)
        self.after_login_screen.btn_mostrar_produto.clicked.connect(self.mostrar_produto)
        self.after_login_screen.btn_mostrar_tecnico.clicked.connect(self.mostrar_tecnico)
        self.after_login_screen.btn_retorno_material.clicked.connect(self.abrir_janela_retorno_material)
        self.after_login_screen.btn_mostrar_produtos_retirados.clicked.connect(self.mostrar_produtos_retirados)
        self.after_login_screen.btn_mostrar_estoque.clicked.connect(self.mostrar_estoque)
        self.login_window.register_button.clicked.connect(self.abrir_tela_register)
        self.after_login_screen.btn_logout.clicked.connect(self.logout)

        self.setCurrentIndex(0)

    def abrir_tela_registro_produto(self):
        try:
            self.material_registration_window = MaterialRegistrationWindow()
            self.material_registration_window.show()
        except Exception as e:
            print(f"Erro ao abrir tela de registro de produto: {e}")

    def abrir_tela_registro_fornecedor(self):
        try:
            self.fornecedor_registration_window = FornecedorRegistrationWindow()
            self.fornecedor_registration_window.show()
        except Exception as e:
            print(f"Erro ao abrir tela de registro de fornecedor: {e}")

    def abrir_tela_registro_tecnico(self):
        try:
            self.tecnico_registration_window = TecnicoRegistrationWindow()
            self.tecnico_registration_window.show()
        except Exception as e:
            print(f"Erro ao abrir tela de registro de técnico: {e}")

    def abrir_tela_register(self):
        if self.register_window is None or not self.register_window.isVisible():
            self.register_window = RegisterWindow(self)
            self.register_window.register_window_closed.connect(self.on_register_window_closed)
        self.register_window.show()

    def on_register_window_closed(self):
        self.register_window = None  # Limpa a variável quando a janela é fechada

    def mostrar_produto(self):
        try:
            self.show_products_window = ShowProductsWindow()
            self.show_products_window.show()
        except Exception as e:
            print(f"Erro ao mostrar produtos: {e}")

    def mostrar_tecnico(self):
        try:
            self.show_tecnico_window = ShowTecnicoWindow()
            self.show_tecnico_window.show()
        except Exception as e:
            print(f'Erro ao mostrar Técnicos: {e}')

    def abrir_janela_retirar_material(self):
        try:
            self.material_withdraw_window = MaterialWithdrawWindow()
            self.material_withdraw_window.show()
        except Exception as e:
            print(f"Erro ao abrir janela de retirada de material: {e}")

    def abrir_janela_retorno_material(self):
        try:
            self.retorno_material_window = RetornoMaterialWindow()
            self.retorno_material_window.show()
        except Exception as e:
            print(f"Erro ao abrir janela de retorno de material: {e}")

    def mostrar_produtos_retirados(self):
        try:
            self.show_withdrawals_window = ShowWithdrawalsWindow()
            self.show_withdrawals_window.show()
        except Exception as e:
            print(f"Erro ao mostrar produtos retirados: {e}")

    def mostrar_estoque(self):
        try:
            self.show_estoque_window = ShowStockWindow()
            self.show_estoque_window.show()
        except Exception as e:
            print(f"Erro ao mostrar estoque: {e}")

    def logout(self):
        self.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
