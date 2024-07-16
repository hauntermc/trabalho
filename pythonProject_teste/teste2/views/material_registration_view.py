from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from controllers.material_controller import register_material
from datetime import datetime, date

class MaterialRegistrationWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.nome = QLineEdit(self)
        self.nome.setPlaceholderText('Nome do Material')
        layout.addWidget(self.nome)

        self.preco = QLineEdit(self)
        self.preco.setPlaceholderText('Preço')
        layout.addWidget(self.preco)

        self.nota_fiscal = QLineEdit(self)
        self.nota_fiscal.setPlaceholderText('Nota Fiscal')
        layout.addWidget(self.nota_fiscal)

        self.quantidade = QLineEdit(self)
        self.quantidade.setPlaceholderText('Quantidade')
        layout.addWidget(self.quantidade)

        self.fornecedora = QLineEdit(self)
        self.fornecedora.setPlaceholderText('Fornecedora')
        layout.addWidget(self.fornecedora)

        self.data = QLineEdit(self)
        self.data.setPlaceholderText('Data (DD/MM/AAAA)')
        self.data.setInputMask('99/99/9999')  # Define a máscara de entrada para data
        layout.addWidget(self.data)

        self.register_button = QPushButton('Registrar Material', self)
        self.register_button.clicked.connect(self.register_material)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register_material(self):
        nome = self.nome.text()
        preco_text = self.preco.text()
        nota_fiscal = self.nota_fiscal.text()
        quantidade_text = self.quantidade.text()
        fornecedora = self.fornecedora.text()
        data_text = self.data.text()

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

        # Chama register_material passando cnpj=None para criar fornecedor sem CNPJ
        try:
            if register_material(nome, preco, nota_fiscal, quantidade, fornecedora, data):
                QMessageBox.information(self, 'Sucesso', 'Material registrado com sucesso.')
            else:
                QMessageBox.critical(self, 'Erro', 'Erro ao registrar material.')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao registrar material: {str(e)}')
