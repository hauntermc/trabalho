from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class AfterLoginScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Botão para abrir a tela de registro de produtos
        self.btn_registrar_produto = QPushButton('Registrar Produto')
        layout.addWidget(self.btn_registrar_produto)

        # Botão para abrir a tela de registro de fornecedores

        self.setLayout(layout)
