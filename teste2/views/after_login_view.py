from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy

class AfterLoginScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Primeira linha de botões
        h_layout1 = QHBoxLayout()
        self.btn_registrar_produto = QPushButton('Registrar Produto')
        self.btn_registrar_fornecedor = QPushButton('Registrar Fornecedor')
        self.btn_registrar_tecnico = QPushButton('Registrar Tecnico')
        h_layout1.addWidget(self.btn_registrar_produto)
        h_layout1.addWidget(self.btn_registrar_fornecedor)
        h_layout1.addWidget(self.btn_registrar_tecnico)
        main_layout.addLayout(h_layout1)

        # Segunda linha de botões
        h_layout2 = QHBoxLayout()
        self.btn_mostrar_produto = QPushButton('Mostrar Produtos')
        self.btn_mostrar_tecnico = QPushButton('Mostrar Tecnico')
        h_layout2.addWidget(self.btn_mostrar_produto)
        h_layout2.addWidget(self.btn_mostrar_tecnico)
        main_layout.addLayout(h_layout2)

        # Terceira linha de botões
        h_layout3 = QHBoxLayout()
        self.btn_retirar_material = QPushButton('Retirar Material')
        self.btn_retorno_material = QPushButton('Retorno de Material')
        h_layout3.addWidget(self.btn_retirar_material)
        h_layout3.addWidget(self.btn_retorno_material)
        main_layout.addLayout(h_layout3)

        # Quarta linha de botões
        h_layout4 = QHBoxLayout()
        self.btn_mostrar_produtos_retirados = QPushButton('Mostrar Produtos Retirados', self)
        self.btn_logout = QPushButton('Logout', self)
        h_layout4.addWidget(self.btn_mostrar_produtos_retirados)
        h_layout4.addWidget(self.btn_logout)
        main_layout.addLayout(h_layout4)

        h_layout5 = QHBoxLayout()
        self.btn_mostrar_estoque = QPushButton('Mostrar Estoque Total', self)
        h_layout5.addWidget(self.btn_mostrar_estoque)
        main_layout.addLayout(h_layout5)

        # Adicionar um espaçador vertical para empurrar os botões para a parte superior
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)

        self.setLayout(main_layout)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = AfterLoginScreen()
    window.show()
    sys.exit(app.exec_())
