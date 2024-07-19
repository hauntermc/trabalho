from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit, QComboBox, QFormLayout
from PyQt5.QtCore import QDate
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Material, Tecnico, RetornoMaterial, engine

Session = sessionmaker(bind=engine)

class RetornoMaterialWindow(QWidget):
    def __init__(self, parent=None):
        super(RetornoMaterialWindow, self).__init__(parent)
        self.setWindowTitle("Retorno de Material")

        # Layout principal
        layout = QVBoxLayout()

        # Layout do formulário
        self.form_layout = QFormLayout()

        # Ordem de Serviço
        self.ordem_servico_label = QLabel("Ordem de Serviço:")
        self.ordem_servico_input = QLineEdit()
        self.form_layout.addRow(self.ordem_servico_label, self.ordem_servico_input)

        # Seleção de Produto
        self.produto_label = QLabel("Selecionar Produto:")
        self.cmb_produto = QComboBox()
        self.form_layout.addRow(self.produto_label, self.cmb_produto)

        # ID do Técnico
        self.tecnico_id_label = QLabel("ID do Técnico:")
        self.tecnico_id_input = QLineEdit()
        self.form_layout.addRow(self.tecnico_id_label, self.tecnico_id_input)

        # Quantidade
        self.quantidade_label = QLabel("Quantidade:")
        self.quantidade_input = QLineEdit()
        self.form_layout.addRow(self.quantidade_label, self.quantidade_input)

        # Data de Retorno
        self.data_retorno_label = QLabel("Data de Retorno:")
        self.data_retorno_input = QDateEdit()
        self.data_retorno_input.setDate(QDate.currentDate())
        self.form_layout.addRow(self.data_retorno_label, self.data_retorno_input)

        # Botão de Enviar
        self.submit_button = QPushButton("Registrar Retorno")
        self.submit_button.clicked.connect(self.registrar_retorno)
        layout.addWidget(self.submit_button)

        # Adicionar o layout do formulário ao layout principal
        layout.addLayout(self.form_layout)
        self.setLayout(layout)

        # Preencher o QComboBox com produtos
        self.populate_produtos()

    def populate_produtos(self):
        session = Session()
        try:
            produtos = session.query(Material).all()
            self.cmb_produto.addItem("Selecione um produto")  # Item padrão opcional
            for produto in produtos:
                self.cmb_produto.addItem(f"{produto.id} - {produto.nome}", userData=produto.id)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar produtos: {e}")
        finally:
            session.close()

    def registrar_retorno(self):
        ordem_servico = self.ordem_servico_input.text()
        produto_id = self.cmb_produto.currentData()  # Obter o ID do produto selecionado no QComboBox
        tecnico_id = self.tecnico_id_input.text()
        quantidade = self.quantidade_input.text()
        data_retorno = self.data_retorno_input.date().toPyDate()

        if not ordem_servico or produto_id is None or not tecnico_id or not quantidade:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            produto_id = int(produto_id)
            tecnico_id = int(tecnico_id)
            quantidade = int(quantidade)
        except ValueError:
            QMessageBox.warning(self, "Erro", "IDs e Quantidade devem ser números inteiros.")
            return

        session = Session()

        try:
            produto = session.query(Material).filter_by(id=produto_id).first()
            if produto is None:
                QMessageBox.warning(self, "Erro", "Produto não encontrado.")
                return

            tecnico = session.query(Tecnico).filter_by(id=tecnico_id).first()
            if tecnico is None:
                QMessageBox.warning(self, "Erro", "Técnico não encontrado.")
                return

            retorno = RetornoMaterial(
                ordem_servico=ordem_servico,
                produto_id=produto_id,
                tecnico_id=tecnico_id,
                quantidade=quantidade,
                data_retorno=data_retorno,
                data=datetime.utcnow().date()  # Adiciona a data atual
            )
            session.add(retorno)

            produto.quantidade += quantidade
            session.commit()

            QMessageBox.information(self, "Sucesso", "Retorno registrado com sucesso.")
            self.close()

        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Erro", f"Erro ao registrar retorno: {e}")

        finally:
            session.close()
