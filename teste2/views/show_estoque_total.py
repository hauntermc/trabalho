#view/show_estoque_total.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Material
from utils.db_utils import Session

class ShowStockWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Estoque Total')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel('Estoque Total', self)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)  # Número de colunas

        headers = ['ID', 'Nome', 'Quantidade']
        self.table_widget.setHorizontalHeaderLabels(headers)

        layout.addWidget(self.table_widget)

        update_button = QPushButton('Atualizar Lista', self)
        update_button.clicked.connect(self.update_stock_list)
        layout.addWidget(update_button)

        close_button = QPushButton('Fechar')
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        # Atualize a lista de estoque ao exibir a janela
        self.update_stock_list()

    def update_stock_list(self):
        try:
            with Session() as session:
                materiais = session.query(Material).all()
                print(f"Materiais recuperados: {[material.nome for material in materiais]}")
                self.update_table(materiais)
        except Exception as e:
            print(f"Erro ao buscar estoque: {e}")
    def update_table(self, materiais):
        self.table_widget.setRowCount(len(materiais))

        for row, material in enumerate(materiais):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(material.id)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(material.nome))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(material.quantidade)))

