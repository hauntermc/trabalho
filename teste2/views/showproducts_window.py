from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from models import Material, Fornecedor
from utils.db_utils import Session
from PyQt5.QtCore import Qt

class ShowProductsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Produtos Registrados')
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Título da janela
        title_label = QLabel('Produtos Registrados', self)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Tabela para exibir produtos
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)  # Número de colunas

        # Definindo os cabeçalhos da tabela
        headers = ['ID', 'Nome', 'Preço', 'Nota Fiscal', 'Quantidade', 'Data', 'Fornecedor']
        self.table_widget.setHorizontalHeaderLabels(headers)

        layout.addWidget(self.table_widget)

        # Botão para atualizar a lista de produtos
        update_button = QPushButton('Atualizar Lista', self)
        update_button.clicked.connect(self.update_product_list)
        layout.addWidget(update_button)

        close_button = QPushButton('Fechar')
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        # Atualizar a lista de produtos ao exibir a janela
        self.update_product_list()

    def update_product_list(self):
        try:
            session = Session()
            produtos = session.query(Material).all()

            self.table_widget.setRowCount(len(produtos))

            for row, produto in enumerate(produtos):
                # Convertendo a data para string formatada
                data_formatada = produto.data.strftime('%d/%m/%Y')

                # Obtendo o nome do fornecedor
                fornecedor = session.query(Fornecedor).filter_by(id=produto.fornecedor_id).first()

                self.table_widget.setItem(row, 0, QTableWidgetItem(str(produto.id)))
                self.table_widget.setItem(row, 1, QTableWidgetItem(produto.nome))
                self.table_widget.setItem(row, 2, QTableWidgetItem(str(produto.preco)))
                self.table_widget.setItem(row, 3, QTableWidgetItem(produto.nota_fiscal))
                self.table_widget.setItem(row, 4, QTableWidgetItem(str(produto.quantidade)))
                self.table_widget.setItem(row, 5, QTableWidgetItem(data_formatada))
                self.table_widget.setItem(row, 6, QTableWidgetItem(fornecedor.nome if fornecedor else 'Não encontrado'))

            session.close()
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")

# Teste da janela de produtos
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ShowProductsWindow()
    window.show()
    sys.exit(app.exec_())
