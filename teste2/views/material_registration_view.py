from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel
from controllers.material_controller import register_material
from datetime import datetime

class MaterialRegistrationWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label_nome = QLabel('Nome do Material')
        self.nome_input = QLineEdit(self)
        layout.addWidget(label_nome)
        layout.addWidget(self.nome_input)

        label_preco = QLabel('Preço')
        self.preco_input = QLineEdit(self)
        layout.addWidget(label_preco)
        layout.addWidget(self.preco_input)

        label_nota_fiscal = QLabel('Nota Fiscal')
        self.nota_fiscal_input = QLineEdit(self)
        layout.addWidget(label_nota_fiscal)
        layout.addWidget(self.nota_fiscal_input)

        label_quantidade = QLabel('Quantidade')
        self.quantidade_input = QLineEdit(self)
        layout.addWidget(label_quantidade)
        layout.addWidget(self.quantidade_input)

        label_fornecedora = QLabel('Fornecedora')
        self.fornecedora_input = QLineEdit(self)
        layout.addWidget(label_fornecedora)
        layout.addWidget(self.fornecedora_input)

        label_data = QLabel('Data (DD/MM/AAAA)')
        self.data_input = QLineEdit(self)
        self.data_input.setInputMask('99/99/9999')  # Define a máscara de entrada para data
        layout.addWidget(label_data)
        layout.addWidget(self.data_input)

        self.register_button = QPushButton('Registrar Material', self)
        self.register_button.clicked.connect(self.register_material)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register_material(self):
        nome = self.nome_input.text()
        preco_text = self.preco_input.text()
        nota_fiscal = self.nota_fiscal_input.text()
        quantidade_text = self.quantidade_input.text()
        fornecedora = self.fornecedora_input.text()
        data_text = self.data_input.text()

        # Validação dos campos numéricos
        try:
            preco = float(preco_text)
            quantidade = int(quantidade_text)
        except ValueError:
            QMessageBox.critical(self, 'Erro', 'Preço e Quantidade devem ser números válidos.')
            return

        # Verifica se a data está no formato correto 'DD/MM/YYYY' e converte para date
        try:
            data = datetime.strptime(data_text, '%d/%m/%Y').date()
        except ValueError:
            QMessageBox.critical(self, 'Erro', 'Formato de data inválido. Use o formato DD/MM/AAAA.')
            return

        try:
            if register_material(nome, preco, nota_fiscal, quantidade, fornecedora, data):
                QMessageBox.information(self, 'Sucesso', 'Material registrado com sucesso.')
                self.nome_input.clear()
                self.preco_input.clear()
                self.nota_fiscal_input.clear()
                self.quantidade_input.clear()
                self.fornecedora_input.clear()
                self.data_input.clear()
            else:
                QMessageBox.critical(self, 'Erro', 'Erro ao registrar material.')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao registrar material: {str(e)}')
