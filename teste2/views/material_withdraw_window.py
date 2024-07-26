import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QFormLayout
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression
from datetime import datetime
from sqlalchemy import func
from utils.db_utils import Session
from models import Material, Tecnico, RetiradaMaterial

class MaterialWithdrawWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Retirar Material')
        self.setGeometry(200, 200, 400, 350)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

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

        self.lbl_data = QLabel('Data (dd/mm/aaaa):')
        self.txt_data = QLineEdit()
        self.set_date_validator()
        self.form_layout.addRow(self.lbl_data, self.txt_data)

        self.lbl_local = QLabel('Local de Utilização:')
        self.txt_local = QLineEdit()
        self.form_layout.addRow(self.lbl_local, self.txt_local)

        self.lbl_ordem_servico = QLabel('Código da Ordem de Serviço:')
        self.txt_ordem_servico = QLineEdit()
        self.form_layout.addRow(self.lbl_ordem_servico, self.txt_ordem_servico)

        self.lbl_patrimonio = QLabel('Patrimônio:')
        self.txt_patrimonio = QLineEdit()
        self.form_layout.addRow(self.lbl_patrimonio, self.txt_patrimonio)

        layout.addLayout(self.form_layout)

        btn_retirar = QPushButton('Retirar')
        btn_retirar.clicked.connect(self.retirar_material)
        layout.addWidget(btn_retirar)

        self.setLayout(layout)

        self.load_products()
        self.load_tecnicos()

        self.setStyleSheet("""
            QWidget {
                background-color: #e6f7ff;  /* Azul claro */
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #003d7a;  /* Azul escuro */
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                padding: 10px;
                border: 1px solid #003d7a;  /* Azul escuro */
                border-radius: 5px;
                background-color: #ffffff;  /* Branco */
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #003d7a;  /* Azul escuro */
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #00264d;  /* Azul mais escuro */
            }
        """)

    def set_date_validator(self):
        # Define a expressão regular para o formato dd/mm/aaaa
        date_regex = QRegularExpression(r'\d{0,2}/?\d{0,2}/?\d{0,4}')
        # Define o validador
        date_validator = QRegularExpressionValidator(date_regex, self)
        self.txt_data.setValidator(date_validator)

        # Conectar o evento de edição para formatar a data
        self.txt_data.textChanged.connect(self.format_date)

    def format_date(self):
        text = self.txt_data.text()
        # Remove todas as barras
        text = text.replace('/', '')
        # Adiciona as barras no formato dd/mm/aaaa
        if len(text) > 2:
            text = f"{text[:2]}/{text[2:]}"
        if len(text) > 5:
            text = f"{text[:5]}/{text[5:]}"
        self.txt_data.setText(text)
        # Move o cursor para o final do texto
        self.txt_data.setCursorPosition(len(text))

    def load_products(self):
        try:
            session = Session()
            produtos = session.query(
                Material.id,  # Adiciona o ID do produto para referência
                Material.nome,
                func.sum(Material.quantidade).label('total_quantidade'),
                Material.patrimonio
            ).group_by(Material.id).all()

            for produto_id, produto_nome, total_quantidade, patrimonio in produtos:
                self.cmb_produto.addItem(f"{produto_nome} ({total_quantidade} - Patrimônio: {patrimonio})", produto_id)
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao carregar produtos: {e}')
        finally:
            session.close()

    def load_tecnicos(self):
        try:
            session = Session()
            tecnicos = session.query(Tecnico).all()
            for tecnico in tecnicos:
                # Adiciona o técnico com o formato Nome (Matrícula: matrícula)
                self.cmb_tecnico.addItem(f"{tecnico.nome} (Matrícula: {tecnico.matricula})", tecnico.id)
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao carregar técnicos: {e}')
        finally:
            session.close()

    def retirar_material(self):
        session = None
        try:
            quantidade_text = self.txt_quantidade.text()
            if not quantidade_text:
                QMessageBox.warning(self, 'Erro', 'O campo de quantidade não pode estar vazio!')
                return

            try:
                quantidade = int(quantidade_text)
            except ValueError:
                QMessageBox.warning(self, 'Erro', 'Quantidade inválida! Deve ser um número inteiro.')
                return

            produto_id = self.cmb_produto.currentData()  # Use o ID do produto
            tecnico_id = self.cmb_tecnico.currentData()
            data_text = self.txt_data.text()
            local = self.txt_local.text()
            ordem_servico = self.txt_ordem_servico.text()
            patrimonio = self.txt_patrimonio.text()

            if not (produto_id and tecnico_id and data_text and local and ordem_servico):
                QMessageBox.warning(self, 'Erro', 'Todos os campos obrigatórios devem ser preenchidos!')
                return

            try:
                data = datetime.strptime(data_text, "%d/%m/%Y").date()
            except ValueError:
                QMessageBox.warning(self, 'Erro', 'Data inválida. Use o formato dd/mm/aaaa.')
                return

            session = Session()

            existing_retirada = session.query(RetiradaMaterial).filter_by(ordem_servico=ordem_servico).first()
            if existing_retirada:
                QMessageBox.warning(self, 'Erro', 'Ordem de serviço já existe!')
                return

            produto = session.query(Material).filter_by(id=produto_id).first()  # Busca o produto pelo ID

            if produto:
                if produto.patrimonio:
                    if patrimonio != produto.patrimonio:
                        QMessageBox.warning(self, 'Erro',
                                            'Patrimônio informado não corresponde ao patrimônio registrado!')
                        return

                if quantidade <= produto.quantidade:
                    produto.quantidade -= quantidade

                    retirada = RetiradaMaterial(
                        codigo=ordem_servico,
                        ordem_servico=ordem_servico,
                        produto_id=produto.id,
                        tecnico_id=tecnico_id,
                        quantidade=quantidade,
                        data=data,
                        local=local,
                        patrimonio=patrimonio or None,  # Se o patrimônio estiver vazio, use None
                        devolvido=False
                    )
                    session.add(retirada)
                    session.commit()

                    QMessageBox.information(self, 'Sucesso',
                                            f'{quantidade} unidades de {produto.nome} retiradas com sucesso! Patrimônio: {produto.patrimonio}')
                    self.clear_fields()  # Limpa os campos após sucesso
                    self.update_products()  # Atualiza a lista de produtos
                else:
                    QMessageBox.warning(self, 'Erro', 'Quantidade solicitada maior do que a disponível!')
            else:
                QMessageBox.warning(self, 'Erro', 'Produto não encontrado!')

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao retirar material: {e}')
            import traceback
            traceback.print_exc()
        finally:
            if session:
                session.close()
    def update_products(self):
        try:
            session = Session()
            self.cmb_produto.clear()  # Limpa a lista atual

            produtos = session.query(
                Material.id,  # Adiciona o ID do produto para referência
                Material.nome,
                func.sum(Material.quantidade).label('total_quantidade'),
                Material.patrimonio
            ).group_by(Material.id).all()

            for produto_id, produto_nome, total_quantidade, patrimonio in produtos:
                self.cmb_produto.addItem(f"{produto_nome} ({total_quantidade} - Patrimônio: {patrimonio})", produto_id)
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao atualizar produtos: {e}')
        finally:
            session.close()

    def clear_fields(self):
        self.cmb_produto.setCurrentIndex(-1)
        self.cmb_tecnico.setCurrentIndex(-1)
        self.txt_quantidade.clear()
        self.txt_data.clear()
        self.txt_local.clear()
        self.txt_ordem_servico.clear()
        self.txt_patrimonio.clear()
