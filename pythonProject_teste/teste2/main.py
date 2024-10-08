import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from views.login_view import LoginWindow
from views.after_login_view import AfterLoginScreen
from views.material_registration_view import MaterialRegistrationWindow

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.login_window = LoginWindow(self)
        self.after_login_screen = AfterLoginScreen()

        self.addWidget(self.login_window)          # Index 0
        self.addWidget(self.after_login_screen)    # Index 1

        self.after_login_screen.btn_registrar_produto.clicked.connect(self.abrir_tela_registro_produto)

        self.setCurrentIndex(0)

    def abrir_tela_registro_produto(self):
        try:
            self.material_registration_window = MaterialRegistrationWindow()
            self.material_registration_window.show()  # Mostra a janela de registro de produtos
        except Exception as e:
            print(f"Erro ao abrir tela de registro de produto: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
