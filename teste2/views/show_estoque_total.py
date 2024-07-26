from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPalette
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, or_
from models import Material
from utils.db_utils import Session

class ShowStockWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Estoque Total')
        self.setGeometry(100, 100, 900, 600)  # Ajuste o tamanho da janela
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Configuração da fonte e paleta de cores
        font = QFont('Arial', 12)
        self.setFont(font)
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor('#f0f0f0'))
        self.setPalette(palette)

        # Título
        title_frame = QFrame(self)
        title_frame.setFrameShape(QFrame.StyledPanel)
        title_frame.setFrameShadow(QFrame.Raised)
        title_frame.setLineWidth(2)
        title_frame.setMidLineWidth(2)
        title_layout = QVBoxLayout()
        title_label = QLabel('Estoque Total', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setStyleSheet('color: #333333')
        title_layout.addWidget(title_label)
        title_frame.setLayout(title_layout)
        layout.addWidget(title_frame)

        # Barra de pesquisa
        search_frame = QFrame(self)
        search_frame.setFrameShape(QFrame.StyledPanel)
        search_frame.setFrameShadow(QFrame.Raised)
        search_frame.setLineWidth(1)
        search_frame.setMidLineWidth(1)
        search_layout = QHBoxLayout()
        search_label = QLabel('Pesquisar:', self)
        search_label.setFont(QFont('Arial', 12))
        self.search_line_edit = QLineEdit(self)
        self.search_line_edit.setPlaceholderText('Digite o nome do material...')
        self.search_line_edit.setFont(QFont('Arial', 12))
        search_button = QPushButton('Buscar', self)
        search_button.setFont(QFont('Arial', 12))
        search_button.setStyleSheet('background-color: #4CAF50; color: white; border: none; border-radius: 5px; padding: 5px 10px;')
        search_button.clicked.connect(self.update_stock_list)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_line_edit)
        search_layout.addWidget(search_button)

        search_frame.setLayout(search_layout)
        layout.addWidget(search_frame)

        # Tabela
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)  # Atualizado para 3 colunas
        headers = ['Nome', 'Quantidade Total', 'Estoque Mínimo']
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setStyleSheet('background-color: #f0f0f0; border: 1px solid #dddddd;')
        self.table_widget.setStyleSheet('background-color: white; border: 1px solid #dddddd;')
        layout.addWidget(self.table_widget)

        # Botões
        button_layout = QHBoxLayout()
        update_button = QPushButton('Atualizar Lista', self)
        update_button.setFont(QFont('Arial', 12))
        update_button.setStyleSheet('background-color: #2196F3; color: white; border: none; border-radius: 5px; padding: 5px 10px;')
        update_button.clicked.connect(self.update_stock_list)

        show_all_stock_button = QPushButton('Mostrar Estoque Crítico e de Aviso', self)
        show_all_stock_button.setFont(QFont('Arial', 12))
        show_all_stock_button.setStyleSheet('background-color: #FF5722; color: white; border: none; border-radius: 5px; padding: 5px 10px;')
        show_all_stock_button.clicked.connect(self.show_all_stock)

        close_button = QPushButton('Fechar', self)
        close_button.setFont(QFont('Arial', 12))
        close_button.setStyleSheet('background-color: #4CAF50; color: white; border: none; border-radius: 5px; padding: 5px 10px;')
        close_button.clicked.connect(self.close)

        button_layout.addWidget(update_button)
        button_layout.addWidget(show_all_stock_button)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

        # Atualize a lista de estoque ao exibir a janela
        self.update_stock_list()

    def update_stock_list(self):
        try:
            search_text = self.search_line_edit.text().lower()
            with Session() as session:
                query = session.query(
                    Material.nome,
                    func.sum(Material.quantidade).label('total_quantidade'),
                    func.min(Material.estoque_minimo).label('min_estoque_minimo')
                ).group_by(Material.nome)

                if search_text:
                    query = query.filter(Material.nome.ilike(f'%{search_text}%'))

                self.materiais = query.all()
                print(f"Materiais recuperados: {[material.nome for material in self.materiais]}")
                self.update_table(self.materiais)
        except Exception as e:
            print(f"Erro ao buscar estoque: {e}")

    def show_all_stock(self):
        try:
            search_text = self.search_line_edit.text().lower()
            with Session() as session:
                subquery = session.query(
                    Material.nome,
                    func.sum(Material.quantidade).label('total_quantidade'),
                    func.min(Material.estoque_minimo).label('min_estoque_minimo')
                ).group_by(Material.nome).subquery()

                query = session.query(
                    subquery.c.nome,
                    subquery.c.total_quantidade,
                    subquery.c.min_estoque_minimo
                ).filter(
                    or_(
                        subquery.c.total_quantidade <= subquery.c.min_estoque_minimo,
                        subquery.c.total_quantidade > subquery.c.min_estoque_minimo,
                        subquery.c.total_quantidade <= subquery.c.min_estoque_minimo * 1.5
                    )
                )

                if search_text:
                    query = query.filter(subquery.c.nome.ilike(f'%{search_text}%'))

                materiais = query.all()
                print(f"Materiais com estoque crítico e de aviso: {[material[0] for material in materiais]}")
                self.update_table(materiais)
        except Exception as e:
            print(f"Erro ao buscar estoque crítico e de aviso: {e}")

    def update_table(self, materiais):
        self.table_widget.setRowCount(len(materiais))

        for row, material in enumerate(materiais):
            nome, total_quantidade, min_estoque_minimo = material

            # Adiciona os itens na tabela
            self.table_widget.setItem(row, 0, QTableWidgetItem(nome))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(total_quantidade)))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(min_estoque_minimo)))

            # Aplicar formatação condicional
            if min_estoque_minimo is not None and min_estoque_minimo > 0:
                if total_quantidade <= min_estoque_minimo:
                    self.table_widget.item(row, 1).setBackground(QColor('red'))
                elif total_quantidade <= min_estoque_minimo * 1.5:
                    self.table_widget.item(row, 1).setBackground(QColor('orange'))
                else:
                    self.table_widget.item(row, 1).setBackground(QColor('white'))
            else:
                self.table_widget.item(row, 1).setBackground(QColor('white'))
