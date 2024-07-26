from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel
from controllers.fornecedor_controller import register_fornecedor
from PyQt5.QtCore import Qt

class FornecedorRegistrationWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Registrar Fornecedor')
        self.setGeometry(100, 100, 400, 300)
        self.initUI()
        self.apply_styles()

    def initUI(self):
        layout = QVBoxLayout()

        # Nome do fornecedor
        label_nome = QLabel('Nome do Fornecedor', self)
        self.nome_input = QLineEdit(self)
        layout.addWidget(label_nome)
        layout.addWidget(self.nome_input)

        # CNPJ
        label_cnpj = QLabel('CNPJ', self)
        self.cnpj_input = QLineEdit(self)
        layout.addWidget(label_cnpj)
        layout.addWidget(self.cnpj_input)

        # Botão de registrar
        self.register_button = QPushButton('Registrar Fornecedor', self)
        self.register_button.clicked.connect(self.register_fornecedor)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #e6f7ff;  /* Azul claro */
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #0056b3;  /* Azul escuro */
                margin-bottom: 5px;
            }
            QLineEdit {
                border: 1px solid #0056b3;
                border-radius: 5px;
                padding: 10px;
                background-color: #ffffff;  /* Branco */
                margin-bottom: 15px;
                outline: none;
            }
            QPushButton {
                background-color: #0056b3;  /* Azul escuro */
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                cursor: pointer;
                outline: none;
            }
            QPushButton:hover {
                background-color: #003d7a;  /* Azul mais escuro */
            }
            QPushButton:focus {
                outline: none;
            }
        """)

    def register_fornecedor(self):
        nome = self.nome_input.text()
        cnpj = self.cnpj_input.text() if self.cnpj_input.text() else None

        try:
            if register_fornecedor(nome, cnpj):
                QMessageBox.information(self, 'Sucesso', 'Fornecedor registrado com sucesso.')
            else:
                QMessageBox.critical(self, 'Erro', 'Erro ao registrar fornecedor.')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro: {str(e)}')
