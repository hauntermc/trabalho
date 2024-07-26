from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel
from PyQt5.QtCore import Qt
from datetime import datetime
from controllers.material_controller import register_material, is_patrimonio_unique
from models import Material, Fornecedor
from utils.db_utils import Session
from datetime import datetime

class MaterialRegistrationWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Registrar Material')
        self.setGeometry(100, 100, 400, 400)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #e6f7ff;  /* Azul claro */
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #003d7a;  /* Azul escuro */
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #003d7a;  /* Azul escuro */
                border-radius: 5px;
                background-color: #ffffff;  /* Branco */
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #003d7a;  /* Azul escuro */
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #00264d;  /* Azul mais escuro */
            }
        """)

        layout = QVBoxLayout()

        # Nome do material
        label_nome = QLabel('Nome do Material', self)
        self.nome_input = QLineEdit(self)
        layout.addWidget(label_nome)
        layout.addWidget(self.nome_input)

        # Preço
        label_preco = QLabel('Preço', self)
        self.preco_input = QLineEdit(self)
        layout.addWidget(label_preco)
        layout.addWidget(self.preco_input)

        # Nota Fiscal
        label_nota_fiscal = QLabel('Nota Fiscal', self)
        self.nota_fiscal_input = QLineEdit(self)
        layout.addWidget(label_nota_fiscal)
        layout.addWidget(self.nota_fiscal_input)

        # Quantidade
        label_quantidade = QLabel('Quantidade', self)
        self.quantidade_input = QLineEdit(self)
        layout.addWidget(label_quantidade)
        layout.addWidget(self.quantidade_input)

        # Fornecedora
        label_fornecedora = QLabel('Fornecedora', self)
        self.fornecedora_input = QLineEdit(self)
        layout.addWidget(label_fornecedora)
        layout.addWidget(self.fornecedora_input)

        # Patrimônio
        label_patrimonio = QLabel('Patrimônio', self)
        self.patrimonio_input = QLineEdit(self)
        layout.addWidget(label_patrimonio)
        layout.addWidget(self.patrimonio_input)

        # Data
        label_data = QLabel('Data (DD/MM/AAAA)', self)
        self.data_input = QLineEdit(self)
        self.data_input.setInputMask('99/99/9999')  # Define a máscara de entrada para data
        layout.addWidget(label_data)
        layout.addWidget(self.data_input)

        # Botão de registrar
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
        patrimonio = self.patrimonio_input.text()
        data_text = self.data_input.text()

        try:
            preco = float(preco_text)
            quantidade = int(quantidade_text)
        except ValueError:
            QMessageBox.critical(self, 'Erro', 'Preço e Quantidade devem ser números válidos.')
            return

        try:
            data = datetime.strptime(data_text, '%d/%m/%Y').date()
        except ValueError:
            QMessageBox.critical(self, 'Erro', 'Formato de data inválido. Use o formato DD/MM/AAAA.')
            return

        try:
            # Verifica se o patrimônio e a nota fiscal são únicos
            if not is_patrimonio_unique(patrimonio):
                QMessageBox.critical(self, 'Erro', 'Patrimônio já registrado.')
                return

            if not is_nota_fiscal_unique(nota_fiscal):
                QMessageBox.critical(self, 'Erro', 'Nota fiscal já registrada.')
                return

            if register_material(nome, preco, nota_fiscal, quantidade, fornecedora, data, patrimonio):
                QMessageBox.information(self, 'Sucesso', 'Material registrado com sucesso.')
                self.nome_input.clear()
                self.preco_input.clear()
                self.nota_fiscal_input.clear()
                self.quantidade_input.clear()
                self.fornecedora_input.clear()
                self.patrimonio_input.clear()
                self.data_input.clear()

                # Atualize a tabela de estoque, se a janela de estoque estiver aberta
                if hasattr(self.parent(), 'show_estoque_window'):
                    self.parent().show_estoque_window.update_stock_list()
            else:
                QMessageBox.critical(self, 'Erro', 'Erro ao registrar material.')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao registrar material: {str(e)}')

def is_nota_fiscal_unique(nota_fiscal):
    session = None
    try:
        session = Session()
        material = session.query(Material).filter_by(nota_fiscal=nota_fiscal).first()
        return material is None
    except Exception as e:
        print(f"Erro ao verificar nota fiscal: {str(e)}")
        return False
    finally:
        if session:
            session.close()
