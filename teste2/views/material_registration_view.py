from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from datetime import datetime
from controllers.material_controller import register_material, is_patrimonio_unique, is_nota_fiscal_unique
from models import Material
from utils.db_utils import Session

class MaterialRegistrationWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Registrar Material')
        self.setGeometry(100, 100, 400, 400)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #e6f7ff;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #003d7a;
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #003d7a;
                border-radius: 5px;
                background-color: #ffffff;
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #003d7a;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #00264d;
            }
        """)

        layout = QFormLayout()

        self.nome_input = QLineEdit(self)
        self.preco_input = QLineEdit(self)
        self.nota_fiscal_input = QLineEdit(self)
        self.quantidade_input = QLineEdit(self)
        self.fornecedora_input = QLineEdit(self)
        self.patrimonio_input = QLineEdit(self)
        self.data_input = QLineEdit(self)
        self.data_input.setInputMask('99/99/9999')

        # Validadores
        self.preco_validator = QDoubleValidator(0.0, 1000000.0, 2, self)
        self.quantidade_validator = QIntValidator(0, 10000, self)
        self.preco_input.setValidator(self.preco_validator)
        self.quantidade_input.setValidator(self.quantidade_validator)

        layout.addRow(QLabel('Nome do Material'), self.nome_input)
        layout.addRow(QLabel('Preço'), self.preco_input)
        layout.addRow(QLabel('Nota Fiscal'), self.nota_fiscal_input)
        layout.addRow(QLabel('Quantidade'), self.quantidade_input)
        layout.addRow(QLabel('Fornecedora'), self.fornecedora_input)
        layout.addRow(QLabel('Patrimônio'), self.patrimonio_input)
        layout.addRow(QLabel('Data (DD/MM/AAAA)'), self.data_input)

        self.register_button = QPushButton('Registrar Material', self)
        self.register_button.clicked.connect(self.register_material)
        layout.addRow(self.register_button)

        self.setLayout(layout)

    def register_material(self):
        try:
            nome, preco, nota_fiscal, quantidade, fornecedora, patrimonio, data = self.collect_inputs()

            if patrimonio and not is_patrimonio_unique(patrimonio):
                QMessageBox.critical(self, 'Erro', 'Patrimônio já registrado.')
                return

            if not is_nota_fiscal_unique(nota_fiscal):
                QMessageBox.critical(self, 'Erro', 'Nota fiscal já registrada.')
                return

            if register_material(nome, preco, nota_fiscal, quantidade, fornecedora, data, patrimonio):
                QMessageBox.information(self, 'Sucesso', 'Material registrado com sucesso.')
                self.clear_fields()
                if hasattr(self.parent(), 'show_estoque_window'):
                    self.parent().show_estoque_window.update_stock_list()
            else:
                QMessageBox.critical(self, 'Erro', 'Erro ao registrar material.')
        except ValueError as e:
            QMessageBox.critical(self, 'Erro', str(e))
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao registrar material: {str(e)}')

    def collect_inputs(self):
        nome = self.nome_input.text().upper()
        preco_text = self.preco_input.text()
        nota_fiscal = self.nota_fiscal_input.text().upper()
        quantidade_text = self.quantidade_input.text()
        fornecedora = self.fornecedora_input.text().upper()
        patrimonio = self.patrimonio_input.text().upper()
        data_text = self.data_input.text()

        if not all([nome, preco_text, nota_fiscal, quantidade_text, fornecedora, data_text]):
            raise ValueError('Todos os campos devem ser preenchidos.')

        try:
            preco = float(preco_text)
        except ValueError:
            raise ValueError('Preço deve ser um número válido.')

        try:
            quantidade = int(quantidade_text)
        except ValueError:
            raise ValueError('Quantidade deve ser um número inteiro.')

        try:
            data = datetime.strptime(data_text, '%d/%m/%Y').date()
        except ValueError:
            raise ValueError('Formato de data inválido. Use o formato DD/MM/AAAA.')

        return nome, preco, nota_fiscal, quantidade, fornecedora, patrimonio, data

    def clear_fields(self):
        self.nome_input.clear()
        self.preco_input.clear()
        self.nota_fiscal_input.clear()
        self.quantidade_input.clear()
        self.fornecedora_input.clear()
        self.patrimonio_input.clear()
        self.data_input.clear()
