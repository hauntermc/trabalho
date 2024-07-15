from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLineEdit
from sqlalchemy.orm import sessionmaker
from produto_database import iniciar_sessao, Produto, criar_banco_dados  # Importe seu engine SQLAlchemy e modelo Produto


class ShowProductsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Produtos Registrados')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Digite o nome do produto...')
        layout.addWidget(self.search_input)

        self.search_button = QPushButton('Buscar', self)
        self.search_button.clicked.connect(self.load_data)
        layout.addWidget(self.search_button)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        try:
            engine = criar_banco_dados()  # Cria o engine SQLAlchemy
            session = iniciar_sessao(engine)  # Inicia a sessão com o engine

            search_term = self.search_input.text().strip()  # Obtém o termo de busca
            query = session.query(Produto)

            if search_term:
                query = query.filter(Produto.nome.like(f'%{search_term}%'))

            produtos = query.all()

            self.table.setRowCount(len(produtos))
            self.table.setColumnCount(6)  # Ajuste para 6 colunas: ID, Nome, Preço, Nota Fiscal, Data, Quantidade
            self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Preço', 'Nota Fiscal', 'Data', 'Quantidade'])

            for row, produto in enumerate(produtos):
                self.table.setItem(row, 0, QTableWidgetItem(str(produto.id)))
                self.table.setItem(row, 1, QTableWidgetItem(produto.nome))
                self.table.setItem(row, 2, QTableWidgetItem(str(produto.preco)))
                self.table.setItem(row, 3, QTableWidgetItem(produto.nota_fiscal))
                self.table.setItem(row, 4, QTableWidgetItem(str(produto.data)))
                self.table.setItem(row, 5, QTableWidgetItem(str(produto.quantidade)))

            session.close()  # Fecha a sessão ao finalizar

        except Exception as e:
            print(f'Erro ao carregar produtos: {e}')
            QMessageBox.critical(self, 'Erro ao Carregar Produtos',
                                 f'Ocorreu um erro ao carregar produtos:\n\n{str(e)}')

