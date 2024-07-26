from PyQt5.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QGroupBox, QHBoxLayout
from models import Material, Fornecedor
from utils.db_utils import Session
from PyQt5.QtCore import Qt


class ShowProductsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Produtos Registrados')
        self.setGeometry(100, 100, 800, 600)

        self.initUI()
        self.apply_styles()

    def initUI(self):
        layout = QVBoxLayout()

        # Título da janela
        title_label = QLabel('Produtos Registrados', self)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Grupo de Pesquisa
        search_group = QGroupBox('Pesquisar Produto')
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Digite o nome do produto')
        self.search_button = QPushButton('Pesquisar', self)
        self.search_button.clicked.connect(self.search_products)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)

        # Tabela para exibir produtos
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)  # Número de colunas

        # Definindo os cabeçalhos da tabela
        headers = ['ID', 'Nome', 'Preço', 'Nota Fiscal', 'Quantidade', 'Data', 'Fornecedor', 'Patrimônio']
        self.table_widget.setHorizontalHeaderLabels(headers)
        layout.addWidget(self.table_widget)

        # Grupo de Ações
        actions_group = QGroupBox('Ações')
        actions_layout = QHBoxLayout()
        update_button = QPushButton('Atualizar Lista', self)
        update_button.clicked.connect(self.update_product_list)
        close_button = QPushButton('Fechar')
        close_button.clicked.connect(self.close)
        actions_layout.addWidget(update_button)
        actions_layout.addWidget(close_button)
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)

        self.setLayout(layout)

        # Atualizar a lista de produtos ao exibir a janela
        self.update_product_list()

    def apply_styles(self):
        # Estilo geral da aplicação
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel#title_label {
                font-size: 24px;
                font-weight: bold;
                color: #4682b4;
                margin-bottom: 20px;
            }
            QGroupBox {
                border: 1px solid #4682b4;
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
            }
            QGroupBox::title {
                color: #4682b4;
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
            QLineEdit {
                border: 1px solid #4682b4;
                border-radius: 5px;
                padding: 5px;
                margin-right: 10px;
            }
            QPushButton {
                background-color: #4682b4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #5a9bd5;
            }
            QTableWidget {
                border: 1px solid #4682b4;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #4682b4;
                color: white;
                padding: 4px;
                border: 1px solid #4682b4;
            }
        """)

    def search_products(self):
        search_text = self.search_input.text().strip()
        try:
            with Session() as session:
                query = session.query(Material)
                if search_text:
                    query = query.filter(Material.nome.like(f"%{search_text}%"))

                produtos = query.all()
                self.update_table(produtos)
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")

    def update_product_list(self):
        try:
            with Session() as session:
                produtos = session.query(Material).all()
                self.update_table(produtos)
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")

    def update_table(self, produtos):
        self.table_widget.setRowCount(len(produtos))

        for row, produto in enumerate(produtos):
            # Convertendo a data para string formatada
            data_formatada = produto.data.strftime('%d/%m/%Y')

            try:
                with Session() as session:
                    fornecedor = session.query(Fornecedor).filter_by(id=produto.fornecedor_id).first()

            except Exception as e:
                fornecedor = None
                print(f"Erro ao buscar fornecedor: {e}")

            self.table_widget.setItem(row, 0, QTableWidgetItem(str(produto.id)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(produto.nome))
            self.table_widget.setItem(row, 2, QTableWidgetItem(f"{produto.preco:.2f}"))
            self.table_widget.setItem(row, 3, QTableWidgetItem(produto.nota_fiscal))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(produto.quantidade)))
            self.table_widget.setItem(row, 5, QTableWidgetItem(data_formatada))
            self.table_widget.setItem(row, 6, QTableWidgetItem(fornecedor.nome if fornecedor else 'Não encontrado'))
            self.table_widget.setItem(row, 7, QTableWidgetItem(str(produto.patrimonio) if produto.patrimonio else ''))

# Teste da janela de produtos
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ShowProductsWindow()
    window.show()
    sys.exit(app.exec_())
