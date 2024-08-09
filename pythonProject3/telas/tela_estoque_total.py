from PyQt5 import QtWidgets, QtGui
from banco_de_dados import session, Material
from sqlalchemy import func

class TelaEstoque(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Estoque Total')
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Adicionar tabela
        self.tabela_estoque = QtWidgets.QTableWidget()
        self.tabela_estoque.setColumnCount(5)
        self.tabela_estoque.setHorizontalHeaderLabels(['Nome do Produto', 'Quantidade', 'Valor Mínimo', 'Status', 'Salvar'])
        self.tabela_estoque.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Botão para atualizar a tabela
        atualizar_button = QtWidgets.QPushButton('Atualizar Estoque')
        atualizar_button.clicked.connect(self.carregar_dados)

        layout.addWidget(atualizar_button)
        layout.addWidget(self.tabela_estoque)
        self.setLayout(layout)

        # Carregar dados inicialmente
        self.carregar_dados()

    def carregar_dados(self):
        # Limpar dados existentes
        self.tabela_estoque.setRowCount(0)

        # Obter dados agregados dos materiais
        materiais = session.query(
            Material.nome,
            func.sum(Material.quantidade).label('total_quantidade'),
            func.min(Material.valor_minimo).label('min_valor_minimo')
        ).group_by(Material.nome).all()

        for material in materiais:
            row_position = self.tabela_estoque.rowCount()
            self.tabela_estoque.insertRow(row_position)

            # Nome do Produto
            self.tabela_estoque.setItem(row_position, 0, QtWidgets.QTableWidgetItem(material.nome))

            # Quantidade total
            quantidade_item = QtWidgets.QTableWidgetItem(str(material.total_quantidade))
            self.tabela_estoque.setItem(row_position, 1, quantidade_item)

            # Valor Mínimo
            valor_minimo_item = QtWidgets.QLineEdit()
            valor_minimo_item.setText(str(material.min_valor_minimo) if material.min_valor_minimo else '')  # Define o valor mínimo existente
            valor_minimo_item.textChanged.connect(lambda text, row=row_position: self.atualizar_status(row))
            self.tabela_estoque.setCellWidget(row_position, 2, valor_minimo_item)

            # Status
            status_item = QtWidgets.QTableWidgetItem()
            self.tabela_estoque.setItem(row_position, 3, status_item)

            # Botão de Salvar
            salvar_button = QtWidgets.QPushButton('Salvar')
            salvar_button.clicked.connect(lambda checked, row=row_position: self.salvar_valor_minimo(row))
            self.tabela_estoque.setCellWidget(row_position, 4, salvar_button)

            # Atualizar cor do status
            self.atualizar_status(row_position)

    def atualizar_status(self, row):
        valor_minimo_item = self.tabela_estoque.cellWidget(row, 2)
        try:
            valor_minimo = float(valor_minimo_item.text()) if valor_minimo_item.text() else 0
        except ValueError:
            valor_minimo = 0  # Definir 0 se a entrada não for válida

        quantidade_item = self.tabela_estoque.item(row, 1)
        try:
            quantidade = int(quantidade_item.text())
        except ValueError:
            quantidade = 0  # Definir 0 se a entrada não for válida

        status_item = self.tabela_estoque.item(row, 3)
        if quantidade <= valor_minimo:
            status_item.setBackground(QtGui.QColor('red'))
            status_item.setText('Urgente')
        elif quantidade <= 1.5 * valor_minimo:
            status_item.setBackground(QtGui.QColor('yellow'))
            status_item.setText('Alerta')
        else:
            status_item.setBackground(QtGui.QColor('white'))
            status_item.setText('Normal')

    def salvar_valor_minimo(self, row):
        valor_minimo_item = self.tabela_estoque.cellWidget(row, 2)
        try:
            valor_minimo = float(valor_minimo_item.text()) if valor_minimo_item.text() else 0
        except ValueError:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'Valor mínimo inválido.')
            return

        nome_produto = self.tabela_estoque.item(row, 0).text()
        materiais = session.query(Material).filter_by(nome=nome_produto).all()
        if materiais:
            for material in materiais:
                # Atualizar o valor mínimo do material
                material.valor_minimo = valor_minimo
            session.commit()

            # Atualizar o status após a mudança do valor mínimo
            # Atualizar o status apenas da linha específica
            self.atualizar_status(row)

            QtWidgets.QMessageBox.information(self, 'Sucesso', 'Valor mínimo salvo com sucesso!')
