from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from sqlalchemy.orm import Session
from models import RetiradaMaterial, Material, Tecnico
from utils.db_utils import engine
from PyQt5.QtCore import Qt
from datetime import datetime

class ShowWithdrawalsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Produtos Retirados')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Título da janela
        title_label = QLabel('Produtos Retirados', self)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Tabela para exibir retiradas
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)  # Número de colunas

        # Definindo os cabeçalhos da tabela
        headers = ['ID', 'Nome do Material', 'Quantidade', 'Data', 'Usuário', 'Ordem de Serviço', 'Local']
        self.table_widget.setHorizontalHeaderLabels(headers)

        layout.addWidget(self.table_widget)

        # Botão para atualizar a lista de retiradas
        update_button = QPushButton('Atualizar Lista', self)
        update_button.clicked.connect(self.update_withdrawal_list)
        layout.addWidget(update_button)

        close_button = QPushButton('Fechar')
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        # Atualizar a lista de retiradas ao exibir a janela
        self.update_withdrawal_list()

    def update_withdrawal_list(self):
        try:
            session = Session(bind=engine)
            retiradas = session.query(RetiradaMaterial).all()

            self.table_widget.setRowCount(len(retiradas))

            for row, retirada in enumerate(retiradas):
                # Convertendo a data para string formatada
                data_formatada = retirada.data.strftime('%d/%m/%Y')

                # Obtendo o nome do material e do técnico
                material = session.query(Material).filter_by(id=retirada.produto_id).first()
                tecnico = session.query(Tecnico).filter_by(id=retirada.tecnico_id).first()

                self.table_widget.setItem(row, 0, QTableWidgetItem(str(retirada.id)))
                self.table_widget.setItem(row, 1, QTableWidgetItem(material.nome if material else 'Desconhecido'))
                self.table_widget.setItem(row, 2, QTableWidgetItem(str(retirada.quantidade)))
                self.table_widget.setItem(row, 3, QTableWidgetItem(data_formatada))
                self.table_widget.setItem(row, 4, QTableWidgetItem(tecnico.nome if tecnico else 'Desconhecido'))
                self.table_widget.setItem(row, 5, QTableWidgetItem(retirada.ordem_servico))
                self.table_widget.setItem(row, 6, QTableWidgetItem(retirada.local))

            session.close()
        except Exception as e:
            print(f"Erro ao buscar retiradas: {e}")

# Teste da janela de retiradas
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ShowWithdrawalsWindow()
    window.show()
    sys.exit(app.exec_())
