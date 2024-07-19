from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QFormLayout
from PyQt5.QtCore import QDate
from utils.db_utils import Session
from models import Material, Tecnico, RetiradaMaterial  # Adicione RetiradaMaterial aqui
import sys
from datetime import datetime

class MaterialWithdrawWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Retirar Material')
        self.setGeometry(200, 200, 400, 350)  # Aumentar a altura para acomodar o novo campo
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Layout do formulário
        self.form_layout = QFormLayout()
        self.lbl_produto = QLabel('Selecionar Produto:')
        self.cmb_produto = QComboBox()
        self.form_layout.addRow(self.lbl_produto, self.cmb_produto)

        self.lbl_tecnico = QLabel('Selecionar Técnico:')
        self.cmb_tecnico = QComboBox()
        self.form_layout.addRow(self.lbl_tecnico, self.cmb_tecnico)

        self.lbl_quantidade = QLabel('Quantidade a Retirar:')
        self.txt_quantidade = QLineEdit()
        self.form_layout.addRow(self.lbl_quantidade, self.txt_quantidade)

        self.lbl_data = QLabel('Data:')
        self.txt_data = QLineEdit()
        self.form_layout.addRow(self.lbl_data, self.txt_data)

        self.lbl_local = QLabel('Local de Utilização:')
        self.txt_local = QLineEdit()
        self.form_layout.addRow(self.lbl_local, self.txt_local)

        self.lbl_ordem_servico = QLabel('Código da Ordem de Serviço:')
        self.txt_ordem_servico = QLineEdit()
        self.form_layout.addRow(self.lbl_ordem_servico, self.txt_ordem_servico)

        layout.addLayout(self.form_layout)

        btn_retirar = QPushButton('Retirar')
        btn_retirar.clicked.connect(self.retirar_material)
        layout.addWidget(btn_retirar)

        self.setLayout(layout)

        self.load_products()
        self.load_tecnicos()

    def load_products(self):
        try:
            session = Session()
            produtos = session.query(Material).all()
            for produto in produtos:
                self.cmb_produto.addItem(produto.nome, produto.id)
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao carregar produtos: {e}')
        finally:
            session.close()

    def load_tecnicos(self):
        try:
            session = Session()
            tecnicos = session.query(Tecnico).all()
            for tecnico in tecnicos:
                self.cmb_tecnico.addItem(tecnico.nome, tecnico.id)
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao carregar técnicos: {e}')
        finally:
            session.close()

    def retirar_material(self):
        session = None
        try:
            quantidade = int(self.txt_quantidade.text())
            produto_id = self.cmb_produto.currentData()
            tecnico_id = self.cmb_tecnico.currentData()
            data_text = self.txt_data.text()
            local = self.txt_local.text()
            ordem_servico = self.txt_ordem_servico.text()

            if not (quantidade and produto_id and tecnico_id and data_text and local and ordem_servico):
                QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos!')
                return

            # Converter texto de data para objeto date
            try:
                data = datetime.strptime(data_text, "%d/%m/%Y").date()  # Assumindo o formato dia/mês/ano
            except ValueError:
                QMessageBox.warning(self, 'Erro', 'Data inválida. Use o formato dd/mm/aaaa.')
                return

            session = Session()
            produto = session.query(Material).filter_by(id=produto_id).first()

            if produto:
                if quantidade <= produto.quantidade:
                    produto.quantidade -= quantidade

                    retirada = RetiradaMaterial(
                        codigo=ordem_servico,
                        ordem_servico=ordem_servico,
                        produto_id=produto_id,
                        tecnico_id=tecnico_id,
                        quantidade=quantidade,
                        data=data,  # Certifique-se de que data é do tipo date
                        local=local
                    )
                    session.add(retirada)
                    session.commit()
                    QMessageBox.information(self, 'Sucesso', f'{quantidade} unidades retiradas com sucesso!')
                else:
                    QMessageBox.warning(self, 'Erro', 'Quantidade solicitada maior do que a disponível!')
            else:
                QMessageBox.warning(self, 'Erro', 'Produto não encontrado!')

        except ValueError:
            QMessageBox.warning(self, 'Erro', 'Digite uma quantidade válida!')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao retirar material: {e}')
        finally:
            if session:
                session.close()
