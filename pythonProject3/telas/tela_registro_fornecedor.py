from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox
from banco_de_dados import Fornecedor, session

class TelaRegistroFornecedor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.nome_input = QLineEdit()
        self.cnpj_input = QLineEdit()

        layout.addRow('Nome:', self.nome_input)
        layout.addRow('CNPJ:', self.cnpj_input)

        self.save_button = QPushButton('Salvar')
        self.save_button.clicked.connect(self.salvar_fornecedor)

        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.setWindowTitle('Registrar Fornecedor')

    def salvar_fornecedor(self):
        nome = self.nome_input.text()
        cnpj = self.cnpj_input.text()

        if nome:
            try:
                novo_fornecedor = Fornecedor(nome=nome, cnpj=cnpj)
                session.add(novo_fornecedor)
                session.commit()
                QMessageBox.information(self, 'Sucesso', 'Fornecedor registrado com sucesso!')
                self.nome_input.clear()
                self.cnpj_input.clear()
            except Exception as e:
                session.rollback()
                QMessageBox.critical(self, 'Erro', f'Erro ao registrar fornecedor: {e}')
        else:
            QMessageBox.warning(self, 'Erro', 'O campo Nome é obrigatório.')
