from PyQt5.QtWidgets import QLineEdit, QPushButton, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
from sqlalchemy.orm import sessionmaker
from tecnico_database import engine_tecnico, Tecnico  # Importe seu engine SQLAlchemy e modelo Tecnico

class ShowTecnicoWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Técnicos Registrados')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('Digite o nome do Técnico...')
        layout.addWidget(self.search_input)

        self.search_button = QPushButton('Buscar', self)
        self.search_button.clicked.connect(self.load_data)
        layout.addWidget(self.search_button)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        Session = sessionmaker(bind=engine_tecnico)
        session = Session()

        try:
            search_term = self.search_input.text()
            query = session.query(Tecnico)

            if search_term:
                query = query.filter(Tecnico.nome.like(f'%{search_term}%'))

            tecnicos = query.all()

            self.table.setRowCount(len(tecnicos))
            self.table.setColumnCount(3)  # Ajuste o número de colunas conforme necessário
            self.table.setHorizontalHeaderLabels(['Matrícula', 'Nome', 'Telefone'])

            for row, tecnico in enumerate(tecnicos):
                self.table.setItem(row, 0, QTableWidgetItem(tecnico.matricula))
                self.table.setItem(row, 1, QTableWidgetItem(tecnico.nome))
                self.table.setItem(row, 2, QTableWidgetItem(tecnico.telefone))

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao carregar os técnicos: {str(e)}')

        finally:
            session.close()
