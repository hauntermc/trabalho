from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QMessageBox, QDateEdit, QLabel
from PyQt5 import QtWidgets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from produto_database import Produto, Estoque, SaidaMaterial

class SaidaMaterialWindowDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SaidaMaterialWindowDialog, self).__init__()
        self.setWindowTitle('Registrar Saída de Material')
        self.setGeometry(100, 100, 600, 400)  # Defina as dimensões conforme necessário

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Dropdown de Produto
        label_produto = QLabel('Produto:')
        self.produto_combo = QComboBox(self)
        self.carregar_produtos()  # Carregar produtos disponíveis
        layout.addWidget(label_produto)
        layout.addWidget(self.produto_combo)

        # Campo de Técnico
        label_tecnico = QLabel('Nome ou Matrícula do Técnico:')
        self.tecnico_input = QLineEdit(self)
        self.tecnico_input.setPlaceholderText('Nome ou Matrícula do Técnico')
        layout.addWidget(label_tecnico)
        layout.addWidget(self.tecnico_input)

        # Dropdown de Tipo de Saída
        label_tipo_saida = QLabel('Tipo de Saída:')
        self.tipo_saida_combo = QComboBox(self)
        self.tipo_saida_combo.addItems(['SOM', 'TELEFONIA', 'CFTV', 'KIT', 'USO INTERNO', 'CAUTELA'])
        layout.addWidget(label_tipo_saida)
        layout.addWidget(self.tipo_saida_combo)

        # Campo de Ordem de Serviço
        label_ordem_servico = QLabel('Ordem de Serviço:')
        self.ordem_servico_input = QLineEdit(self)
        self.ordem_servico_input.setPlaceholderText('Ordem de Serviço')
        layout.addWidget(label_ordem_servico)
        layout.addWidget(self.ordem_servico_input)

        # Campo de Data da Ordem
        label_data_ordem = QLabel('Data da Ordem:')
        self.data_ordem_input = QDateEdit(self)
        self.data_ordem_input.setDate(date.today())
        layout.addWidget(label_data_ordem)
        layout.addWidget(self.data_ordem_input)

        # Campo de Local de Serviço
        label_local_servico = QLabel('Local de Serviço:')
        self.local_servico_input = QLineEdit(self)
        self.local_servico_input.setPlaceholderText('Local de Serviço')
        layout.addWidget(label_local_servico)
        layout.addWidget(self.local_servico_input)

        # Campo de Patrimônio
        label_patrimonio = QLabel('Patrimônio (opcional):')
        self.patrimonio_input = QLineEdit(self)
        self.patrimonio_input.setPlaceholderText('Patrimônio (opcional)')
        layout.addWidget(label_patrimonio)
        layout.addWidget(self.patrimonio_input)

        # Campo de Quantidade
        label_quantidade = QLabel('Quantidade:')
        self.quantidade_input = QLineEdit(self)
        self.quantidade_input.setPlaceholderText('Quantidade')
        layout.addWidget(label_quantidade)
        layout.addWidget(self.quantidade_input)

        # Botão de Registrar Saída
        registrar_button = QPushButton('Registrar Saída')
        registrar_button.clicked.connect(self.registrar_saida)
        layout.addWidget(registrar_button)

        self.setLayout(layout)

    def carregar_produtos(self):
        engine_produto = create_engine('sqlite:///produtos2.db')
        SessionProduto = sessionmaker(bind=engine_produto)
        self.session_produto = SessionProduto()

        try:
            produtos = self.session_produto.query(Produto).all()
            for produto in produtos:
                self.produto_combo.addItem(produto.nome)

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao carregar os produtos: {str(e)}')

    def validar_quantidade_suficiente(self, produto_id, quantidade):
        engine_estoque = create_engine('sqlite:///estoque_database.db')
        SessionEstoque = sessionmaker(bind=engine_estoque)
        session_estoque = SessionEstoque()

        try:
            estoque_produto = session_estoque.query(Estoque).filter_by(produto_id=produto_id).first()

            if estoque_produto and estoque_produto.quantidade >= quantidade:
                return True
            else:
                return False

        except Exception as e:
            print(f"Erro ao validar quantidade: {e}")
            return False

        finally:
            session_estoque.close()

    def registrar_saida(self):
        engine_saida = create_engine('sqlite:///saida_material.db')
        SessionSaida = sessionmaker(bind=engine_saida)
        session_saida = SessionSaida()

        try:
            nome_produto = self.produto_combo.currentText()
            produto = self.session_produto.query(Produto).filter_by(nome=nome_produto).first()

            if not produto:
                raise ValueError('Produto não encontrado.')

            quantidade = int(self.quantidade_input.text())

            if not self.validar_quantidade_suficiente(produto.id, quantidade):
                raise ValueError('Quantidade insuficiente no estoque.')

            tecnico = self.tecnico_input.text()
            tipo_saida = self.tipo_saida_combo.currentText()
            ordem_servico = self.ordem_servico_input.text()
            data_ordem = self.data_ordem_input.date().toPyDate()
            local_servico = self.local_servico_input.text()
            patrimonio = self.patrimonio_input.text()

            saida_material = SaidaMaterial(
                produto_id=produto.id,
                tecnico=tecnico,
                tipo_saida=tipo_saida,
                ordem_servico=ordem_servico,
                data_ordem=data_ordem,
                local_servico=local_servico,
                patrimonio=patrimonio,
                quantidade=quantidade
            )
            session_saida.add(saida_material)
            session_saida.commit()

            # Atualizar o estoque após a saída
            engine_estoque = create_engine('sqlite:///estoque_database.db')
            SessionEstoque = sessionmaker(bind=engine_estoque)
            session_estoque = SessionEstoque()

            estoque_produto = session_estoque.query(Estoque).filter_by(produto_id=produto.id).first()
            if estoque_produto:
                estoque_produto.quantidade -= quantidade
                session_estoque.commit()

            QMessageBox.information(self, 'Sucesso', 'Saída de material registrada com sucesso!')

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao registrar a saída de material: {str(e)}')

        finally:
            session_saida.close()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = SaidaMaterialWindowDialog()
    dialog.show()
    sys.exit(app.exec_())
