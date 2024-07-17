import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from views.login_view import LoginWindow
from views.after_login_view import AfterLoginScreen
from views.material_registration_view import MaterialRegistrationWindow
from views.fornecedor_registration_view import FornecedorRegistrationWindow
from views.tecnico_registration_view import TecnicoRegistrationWindow
from views.register_view import RegisterWindow

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.login_window = LoginWindow(self)
        self.after_login_screen = AfterLoginScreen()
        #self.register_window = RegisterWindow()

        self.addWidget(self.login_window)          # Index 0
        self.addWidget(self.after_login_screen)    # Index 1
        #self.addWidget(self.register_window)       # Index 2



        self.after_login_screen.btn_registrar_produto.clicked.connect(self.abrir_tela_registro_produto)
        self.after_login_screen.btn_registrar_fornecedor.clicked.connect(self.abrir_tela_registro_fornecedor)
        self.after_login_screen.btn_registrar_tecnico.clicked.connect(self.abrir_tela_registro_tecnico)
        self.login_window.register_button.clicked.connect(self.abrir_tela_register)
        self.after_login_screen.btn_logout.clicked.connect(self.logout)


        self.setCurrentIndex(0)

    def abrir_tela_registro_produto(self):
        try:
            self.material_registration_window = MaterialRegistrationWindow()
            self.material_registration_window.show()  # Mostra a janela de registro de produtos
        except Exception as e:
            print(f"Erro ao abrir tela de registro de produto: {e}")

    def abrir_tela_registro_fornecedor(self):
        try:
            self.fornecedor_registration_window = FornecedorRegistrationWindow()
            self.fornecedor_registration_window.show()
        except Exception as e:
            print(f"Erro ao abrir tela de registro de produto: {e}")

    def abrir_tela_registro_tecnico(self):
        try:
            self.tecnico_registration_window = TecnicoRegistrationWindow()
            self.tecnico_registration_window.show()
        except Exception as e:
            print(f"Erro ao abrir tela de registro de produto: {e}")

    def abrir_tela_register(self):
        try:
            self.register_window = RegisterWindow()
            self.register_window.show()  # Mostra a janela de registro de produtos
        except Exception as e:
            print(f"Erro ao abrir tela de registro : {e}")

    def logout(self):
        self.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
