from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QMessageBox, QDateEdit
from sqlalchemy import create_engine, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date
from estoque_database import Produto, Estoque, SaidaMaterial

Base = declarative_base()

class SaidaMaterialWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Saída de Material')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.produto_combo = QComboBox(self)
        self.carregar_produtos()  # Carregar produtos disponíveis
        layout.addWidget(self.produto_combo)

        self.tecnico_input = QLineEdit(self)
        self.tecnico_input.setPlaceholderText('Nome ou Matrícula do Técnico')
        layout.addWidget(self.tecnico_input)

        self.tipo_saida_combo = QComboBox(self)
        self.tipo_saida_combo.addItems(['SOM', 'TELEFONIA', 'CFTV', 'KIT', 'USO INTERNO', 'CAUTELA'])
        layout.addWidget(self.tipo_saida_combo)

        self.ordem_servico_input = QLineEdit(self)
        self.ordem_servico_input.setPlaceholderText('Ordem de Serviço')
        layout.addWidget(self.ordem_servico_input)

        self.data_ordem_input = QDateEdit(self)
        self.data_ordem_input.setDate(date.today())
        layout.addWidget(self.data_ordem_input)

        self.local_servico_input = QLineEdit(self)
        self.local_servico_input.setPlaceholderText('Local de Serviço')
        layout.addWidget(self.local_servico_input)

        self.patrimonio_input = QLineEdit(self)
        self.patrimonio_input.setPlaceholderText('Patrimônio (opcional)')
        layout.addWidget(self.patrimonio_input)

        self.quantidade_input = QLineEdit(self)
        self.quantidade_input.setPlaceholderText('Quantidade')
        layout.addWidget(self.quantidade_input)

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
            print(f"Produto ID {produto_id}: Estoque encontrado: {estoque_produto}")

            if estoque_produto:
                print(f"Quantidade disponível no estoque: {estoque_produto.quantidade}")
                if estoque_produto.quantidade >= quantidade:
                    return True
                else:
                    return False
            else:
                print("Produto não encontrado no estoque.")
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

        engine_estoque = create_engine('sqlite:///estoque_database.db')
        SessionEstoque = sessionmaker(bind=engine_estoque)
        session_estoque = SessionEstoque()

        try:
            tecnico = self.tecnico_input.text()
            tipo_saida = self.tipo_saida_combo.currentText()
            ordem_servico = self.ordem_servico_input.text()
            data_ordem = self.data_ordem_input.date().toPyDate()
            local_servico = self.local_servico_input.text()
            patrimonio = self.patrimonio_input.text()
            quantidade = int(self.quantidade_input.text())

            nome_produto = self.produto_combo.currentText()
            produto = self.session_produto.query(Produto).filter_by(nome=nome_produto).first()
            print(f"Produto selecionado: {produto.nome} (ID: {produto.id})")

            if not produto:
                raise ValueError('Produto não encontrado.')

            if not self.validar_quantidade_suficiente(produto.id, quantidade):
                raise ValueError('Quantidade insuficiente no estoque.')

            saida_material = SaidaMaterial(tecnico=tecnico, tipo_saida=tipo_saida, ordem_servico=ordem_servico,
                                           data_ordem=data_ordem, local_servico=local_servico, patrimonio=patrimonio,
                                           quantidade=quantidade, produto=produto)

            session_saida.add(saida_material)
            session_saida.commit()

            estoque_produto = session_estoque.query(Estoque).filter_by(produto_id=produto.id).first()
            print(f"Quantidade atual no estoque antes da saída: {estoque_produto.quantidade}")

            if estoque_produto:
                estoque_produto.quantidade -= quantidade
                session_estoque.commit()
                print(f"Quantidade atual no estoque após a saída: {estoque_produto.quantidade}")

            QMessageBox.information(self, 'Sucesso', 'Saída de material registrada com sucesso!')

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao registrar a saída de material: {str(e)}')

        finally:
            session_saida.close()
            session_estoque.close()
