from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from banco_de_dados import session, RetiradaMaterial

class TelaMateriaisRetirados(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Materiais Retirados')
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Tabela para mostrar materiais retirados
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)  # Alterado para 6 colunas para incluir o Patrimônio
        self.table.setHorizontalHeaderLabels(['ID', 'Material ID', 'Nome do Técnico', 'Data Retirada', 'Patrimônio', 'Retornado'])

        # Adicionar tabela ao layout
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Carregar dados na tabela
        self.load_data()

    def load_data(self):
        try:
            # Consultar os materiais retirados
            materiais_retirados = session.query(RetiradaMaterial).all()

            self.table.setRowCount(len(materiais_retirados))
            for row, retirada in enumerate(materiais_retirados):
                self.table.setItem(row, 0, QTableWidgetItem(str(retirada.id)))
                self.table.setItem(row, 1, QTableWidgetItem(str(retirada.material_id)))
                self.table.setItem(row, 2, QTableWidgetItem(retirada.tecnico_nome))
                self.table.setItem(row, 3, QTableWidgetItem(retirada.data_retirada.strftime('%Y-%m-%d %H:%M:%S')))
                self.table.setItem(row, 4, QTableWidgetItem(retirada.patrimonio))  # Nova coluna para Patrimônio
                retornado_text = 'Sim' if retirada.retornado else 'Não'
                self.table.setItem(row, 5, QTableWidgetItem(retornado_text))  # Coluna ajustada para o status "Retornado"
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao carregar os dados: {str(e)}')

