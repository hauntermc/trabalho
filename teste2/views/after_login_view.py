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

        # Botão pra abrir a tela de registro de fornecedor
        self.btn_registrar_fornecedor = QPushButton('Registrar Fornecedor')
        layout.addWidget(self.btn_registrar_fornecedor)

        self.btn_registrar_tecnico = QPushButton('Registrar Tecnico')
        layout.addWidget(self.btn_registrar_tecnico)

        self.btn_mostrar_produto = QPushButton('Mostrar Produtos')
        layout.addWidget(self.btn_mostrar_produto)

        self.btn_mostrar_tecnico = QPushButton('Mostrar Tecnico')
        layout.addWidget(self.btn_mostrar_tecnico)

        self.btn_retirar_material = QPushButton('Retirar Material')
        layout.addWidget(self.btn_retirar_material)

        self.btn_retorno_material = QPushButton('Retorno de Material')
        layout.addWidget(self.btn_retorno_material)

        self.btn_mostrar_produtos_retirados = QPushButton('Mostrar Produtos Retirados', self)
        layout.addWidget(self.btn_mostrar_produtos_retirados)

        self.btn_logout = QPushButton ('Logout', self)
        layout.addWidget(self.btn_logout)



        self.setLayout(layout)
