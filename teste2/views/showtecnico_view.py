from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from models import Tecnico
from utils.db_utils import Session
from PyQt5.QtCore import Qt

class ShowTecnicoWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Técnicos Registrados')
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label de título
        title_label = QLabel('Lista de Técnicos Registrados')
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Tabela para exibir os técnicos
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)  # Número de colunas: nome, matrícula, telefone
        self.table_widget.setHorizontalHeaderLabels(['Nome', 'Matrícula', 'Telefone'])
        layout.addWidget(self.table_widget)

        # Botão para atualizar a lista de técnicos
        update_button = QPushButton('Atualizar')
        update_button.clicked.connect(self.update_tecnicos)
        layout.addWidget(update_button)

        # Botão para fechar a janela
        close_button = QPushButton('Fechar')
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        # Carregar dados dos técnicos na tabela
        self.update_tecnicos()

    def update_tecnicos(self):
        session = None
        try:
            session = Session()

            # Consulta todos os técnicos no banco de dados
            tecnicos = session.query(Tecnico).all()

            # Limpar tabela antes de atualizar
            self.table_widget.setRowCount(0)

            # Preencher a tabela com os dados dos técnicos
            row = 0
            for tecnico in tecnicos:
                self.table_widget.insertRow(row)
                self.table_widget.setItem(row, 0, QTableWidgetItem(tecnico.nome))
                self.table_widget.setItem(row, 1, QTableWidgetItem(tecnico.matricula))
                self.table_widget.setItem(row, 2, QTableWidgetItem(tecnico.telefone))
                row += 1

        except Exception as e:
            print(f"Erro ao carregar técnicos: {e}")
        finally:
            if session:
                session.close()


