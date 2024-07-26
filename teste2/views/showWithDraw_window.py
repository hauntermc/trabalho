from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from sqlalchemy.orm import Session
from models import RetiradaMaterial, Material, Tecnico
from utils.db_utils import engine
from PyQt5.QtCore import Qt

class ShowWithdrawalsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Produtos Retirados')
        self.setGeometry(100, 100, 900, 600)  # Ajuste a largura para acomodar a nova coluna
        self.initUI()
        self.apply_styles()

    def initUI(self):
        layout = QVBoxLayout()

        # Título da janela
        title_label = QLabel('Produtos Retirados', self)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Tabela para exibir retiradas
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(9)  # Atualize o número de colunas

        # Definindo os cabeçalhos da tabela
        headers = ['ID', 'Nome do Material', 'Quantidade', 'Data', 'Usuário', 'Ordem de Serviço', 'Local', 'Patrimônio', 'Retorno']
        self.table_widget.setHorizontalHeaderLabels(headers)

        layout.addWidget(self.table_widget)

        # Layout horizontal para os botões
        button_layout = QHBoxLayout()

        # Botão para atualizar a lista de retiradas
        update_button = QPushButton('Atualizar Lista', self)
        update_button.clicked.connect(self.update_withdrawal_list)
        update_button.setFocusPolicy(Qt.NoFocus)
        button_layout.addWidget(update_button)

        # Botão para fechar a janela
        close_button = QPushButton('Fechar')
        close_button.clicked.connect(self.close)
        close_button.setFocusPolicy(Qt.NoFocus)
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
            QPushButton:focus {
                outline: none;
            }
            QTableWidget {
                border: 1px solid #4682b4;
                border-radius: 5px;
                selection-background-color: #B0E0E6;
                selection-color: black;
                outline: 0;
            }
            QTableWidget::item {
                outline: none;
            }
            QHeaderView::section {
                background-color: #4682b4;
                color: white;
                padding: 4px;
                border: 1px solid #4682b4;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #4682b4;
            }
        """)

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

                # Adicionando prints para depuração
                print(f"ID: {retirada.id}")
                print(f"Nome do Material: {material.nome if material else 'Desconhecido'}")
                print(f"Quantidade: {retirada.quantidade}")
                print(f"Data: {data_formatada}")
                print(f"Técnico: {tecnico.nome if tecnico else 'Desconhecido'}")
                print(f"Ordem de Serviço: {retirada.ordem_servico}")
                print(f"Local: {retirada.local}")
                print(f"Patrimônio: {retirada.patrimonio}")  # Print para o patrimônio
                print(f"Devolvido: {'Sim' if retirada.devolvido else 'Não'}")

                self.table_widget.setItem(row, 0, QTableWidgetItem(str(retirada.id)))
                self.table_widget.setItem(row, 1, QTableWidgetItem(material.nome if material else 'Desconhecido'))
                self.table_widget.setItem(row, 2, QTableWidgetItem(str(retirada.quantidade)))
                self.table_widget.setItem(row, 3, QTableWidgetItem(data_formatada))
                self.table_widget.setItem(row, 4, QTableWidgetItem(tecnico.nome if tecnico else 'Desconhecido'))
                self.table_widget.setItem(row, 5, QTableWidgetItem(retirada.ordem_servico))
                self.table_widget.setItem(row, 6, QTableWidgetItem(retirada.local))
                self.table_widget.setItem(row, 7, QTableWidgetItem(str(retirada.patrimonio)))  # Converta para string

                # Adicionando a coluna "Devolvido"
                devolvido = 'Sim' if retirada.devolvido else 'Não'
                self.table_widget.setItem(row, 8, QTableWidgetItem(devolvido))  # Atualize o índice da coluna "Devolvido"

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao carregar retiradas: {e}')
        finally:
            session.close()

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
