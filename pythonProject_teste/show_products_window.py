from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
from sqlalchemy.orm import sessionmaker
from produto_database import engine_produto, Produto  # Importe seu engine SQLAlchemy e modelo Produto

class ShowProductsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Produtos Registrados')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        Session = sessionmaker(bind=engine_produto)
        session = Session()

        try:
            produtos = session.query(Produto).all()
            self.table.setRowCount(len(produtos))
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Preço'])

            for row, produto in enumerate(produtos):
                self.table.setItem(row, 0, QTableWidgetItem(str(produto.id)))
                self.table.setItem(row, 1, QTableWidgetItem(produto.nome))
                self.table.setItem(row, 2, QTableWidgetItem(str(produto.preco)))
        except Exception as e:
            print(f'Erro ao carregar produtos: {e}')
        finally:
            session.close()
