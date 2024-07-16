from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from controllers.fornecedor_controller import register_fornecedor

class FornecedorRegistrationWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.nome = QLineEdit(self)
        self.nome.setPlaceholderText('Nome do Fornecedor')
        layout.addWidget(self.nome)

        self.cnpj = QLineEdit(self)
        self.cnpj.setPlaceholderText('CNPJ (opcional)')
        layout.addWidget(self.cnpj)

        self.register_button = QPushButton('Registrar Fornecedor', self)
        self.register_button.clicked.connect(self.register_fornecedor)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register_fornecedor(self):
        nome = self.nome.text()
        cnpj = self.cnpj.text() if self.cnpj.text() else None

        try:
            if register_fornecedor(nome, cnpj):
                QMessageBox.information(self, 'Sucesso', 'Fornecedor registrado com sucesso.')
            else:
                QMessageBox.critical(self, 'Erro', 'Erro ao registrar fornecedor.')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro: {str(e)}')
