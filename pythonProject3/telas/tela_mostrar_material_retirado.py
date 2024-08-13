from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from banco_de_dados import session, RetiradaMaterial

class TelaMateriaisRetirados(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Materiais Retirados')
        self.setGeometry(200, 100, 1300, 400)  # Ajustado para acomodar a nova coluna
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Estilo moderno com cor azul clara
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff; /* Cor de fundo azul clara */
                font-family: Arial, sans-serif;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 2px solid #003366;
                padding: 8px;
                border-radius: 5px;
                gridline-color: #003366;
                font-size: 10pt;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #003366;
                color: white;
                padding: 8px;
                border: none;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #003366;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #0055a5;
            }
            QLabel {
                color: #003366;
                font-weight: bold;
                font-size: 12pt;
            }
        """)

        # Tabela para mostrar materiais retirados
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(9)  # Alterado para 9 colunas
        self.table.setHorizontalHeaderLabels(['ID', 'OS', 'Nome do Material', 'Quantidade', 'Nome do Técnico', 'Data Retirada', 'Patrimônio', 'Local', 'Retornado'])
        # Aumentar o espaçamento entre as colunas
        self.table.horizontalHeader().setDefaultSectionSize(120)  # Largura padrão para todas as colunas
        self.table.setColumnWidth(1, 150)  # Largura específica para a coluna 'OS'
        self.table.setColumnWidth(2, 200)  # Largura específica para a coluna 'Nome do Material'
        self.table.setColumnWidth(4, 150)  # Largura específica para a coluna 'Nome do Técnico'

        # Adicionar tabela ao layout
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Carregar dados na tabela
        self.load_data()

    def load_data(self):
        try:
            # Consultar os materiais retirados e seus materiais associados
            materiais_retirados = session.query(RetiradaMaterial).join(RetiradaMaterial.material).all()

            self.table.setRowCount(len(materiais_retirados))
            for row, retirada in enumerate(materiais_retirados):
                self.table.setItem(row, 0, QTableWidgetItem(str(retirada.id)))
                self.table.setItem(row, 1, QTableWidgetItem(retirada.ordem_servico))
                self.table.setItem(row, 2, QTableWidgetItem(retirada.material.nome))  # Nome do material
                self.table.setItem(row, 3, QTableWidgetItem(retirada.quantidade))
                self.table.setItem(row, 4, QTableWidgetItem(retirada.tecnico_nome))
                self.table.setItem(row, 5, QTableWidgetItem(retirada.data_retirada.strftime('%Y-%m-%d %H:%M:%S')))
                self.table.setItem(row, 6, QTableWidgetItem(retirada.patrimonio))  # Patrimônio
                self.table.setItem(row, 7, QTableWidgetItem(retirada.local_utilizacao))  # Local
                retornado_text = 'Sim' if retirada.retornado else 'Não'
                self.table.setItem(row, 8, QTableWidgetItem(retornado_text))  # Status "Retornado"
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao carregar os dados: {str(e)}')
