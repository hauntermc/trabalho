from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLineEdit
from sqlalchemy.orm import sessionmaker
from fornecedores_database import Fornecedor, engine

class ShowFornecedores(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fornecedores Registrados')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Digite o nome do fornecedor...')
        layout.addWidget(self.search_input)

        self.search_button = QPushButton('Buscar', self)
        self.search_button.clicked.connect(self.load_data)
        layout.addWidget(self.search_button)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            search_term = self.search_input.text()
            query = session.query(Fornecedor)

            if search_term:
                query = query.filter(Fornecedor.nome.like(f'%{search_term}%'))

            fornecedores = query.all()

            # Limpar conteúdo anterior da tabela
            self.table.clearContents()

            self.table.setRowCount(len(fornecedores))
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'CNPJ'])

            for row, fornecedor in enumerate(fornecedores):
                self.table.setItem(row, 0, QTableWidgetItem(str(fornecedor.id)))
                self.table.setItem(row, 1, QTableWidgetItem(fornecedor.nome))
                self.table.setItem(row, 2, QTableWidgetItem(str(fornecedor.cnpj)))

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao carregar os fornecedores: {str(e)}')

        finally:
            session.close()
