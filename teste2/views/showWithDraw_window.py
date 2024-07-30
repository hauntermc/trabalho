from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                             QHBoxLayout, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_
from models import RetiradaMaterial, Material, Tecnico
from utils.db_utils import engine

class ShowWithdrawalsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Produtos Retirados')
        self.setGeometry(100, 100, 900, 600)
        self.initUI()
        self.apply_styles()

    def initUI(self):
        layout = QVBoxLayout()

        # Título da janela
        title_label = QLabel('Produtos Retirados', self)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Barra de pesquisa
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText('Pesquisar por material, técnico, ordem de serviço, etc.')
        search_layout.addWidget(self.search_box)

        search_button = QPushButton('Pesquisar', self)
        search_button.clicked.connect(self.search_withdrawals)
        search_layout.addWidget(search_button)

        layout.addLayout(search_layout)

        # Tabela para exibir retiradas
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(9)
        headers = ['ID', 'Nome do Material', 'Quantidade', 'Data', 'Usuário', 'Ordem de Serviço', 'Local', 'Patrimônio',
                   'Retorno']
        self.table_widget.setHorizontalHeaderLabels(headers)
        layout.addWidget(self.table_widget)

        # Layout horizontal para os botões
        button_layout = QHBoxLayout()
        update_button = QPushButton('Atualizar Lista', self)
        update_button.clicked.connect(self.update_withdrawal_list)
        button_layout.addWidget(update_button)

        close_button = QPushButton('Fechar', self)
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Atualizar a lista de retiradas ao exibir a janela
        self.update_withdrawal_list()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #4682b4;
                margin-bottom: 20px;
            }
            QPushButton {
                background-color: #4682b4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
                outline: none;
            }
            QPushButton:hover {
                background-color: #5a9bd5;
            }
            QLineEdit {
                padding: 5px;
                border-radius: 5px;
                border: 1px solid #4682b4;
                margin: 5px;
            }
            QTableWidget {
                border: 1px solid #4682b4;
                border-radius: 5px;
                selection-background-color: #B0E0E6;
                selection-color: black;
                outline: 0;
            }
            QHeaderView::section {
                background-color: #4682b4;
                color: white;
                padding: 4px;
                border: 1px solid #4682b4;
            }
        """)

    def update_withdrawal_list(self, filter_text=''):
        Session = sessionmaker(bind=engine)
        try:
            with Session() as session:
                query = session.query(RetiradaMaterial).join(Material, RetiradaMaterial.produto_id == Material.id)\
                                                         .join(Tecnico, RetiradaMaterial.tecnico_id == Tecnico.id)

                if filter_text:
                    # Aplicar filtro na consulta
                    query = query.filter(
                        or_(
                            RetiradaMaterial.id.like(f'%{filter_text}%'),
                            Material.nome.like(f'%{filter_text}%'),
                            Tecnico.nome.like(f'%{filter_text}%'),
                            RetiradaMaterial.ordem_servico.like(f'%{filter_text}%')  # Incluindo filtro por Ordem de Serviço
                        )
                    )

                retiradas = query.all()

                self.table_widget.setRowCount(len(retiradas))
                for row, retirada in enumerate(retiradas):
                    material = session.query(Material).filter_by(id=retirada.produto_id).first()
                    tecnico = session.query(Tecnico).filter_by(id=retirada.tecnico_id).first()

                    data_formatada = retirada.data.strftime('%d/%m/%Y')
                    self.table_widget.setItem(row, 0, QTableWidgetItem(str(retirada.id)))
                    self.table_widget.setItem(row, 1, QTableWidgetItem(material.nome if material else 'Desconhecido'))
                    self.table_widget.setItem(row, 2, QTableWidgetItem(str(retirada.quantidade)))
                    self.table_widget.setItem(row, 3, QTableWidgetItem(data_formatada))
                    self.table_widget.setItem(row, 4, QTableWidgetItem(tecnico.nome if tecnico else 'Desconhecido'))
                    self.table_widget.setItem(row, 5, QTableWidgetItem(retirada.ordem_servico))
                    self.table_widget.setItem(row, 6, QTableWidgetItem(retirada.local))
                    self.table_widget.setItem(row, 7, QTableWidgetItem(str(retirada.patrimonio)))
                    self.table_widget.setItem(row, 8, QTableWidgetItem('Sim' if retirada.devolvido else 'Não'))

                self.table_widget.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao carregar retiradas: {e}')

    def search_withdrawals(self):
        filter_text = self.search_box.text()
        self.update_withdrawal_list(filter_text)

    def connect_return_window(self, return_window):
        return_window.material_returned.connect(self.update_withdrawal_list)


# Teste da janela de retiradas
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ShowWithdrawalsWindow()
    window.show()
    sys.exit(app.exec_())
