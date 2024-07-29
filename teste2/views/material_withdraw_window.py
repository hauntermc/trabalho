from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, QComboBox
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from utils.db_utils import Session
from models import Material, Tecnico, RetiradaMaterial

class MaterialWithdrawWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Retirar Material')
        self.setGeometry(200, 200, 500, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.form_layout = QFormLayout()

        # ComboBox para produtos
        self.cmb_produto = QComboBox()
        self.cmb_produto.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #003d7a;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border-left: 1px solid #003d7a;
                padding-right: 5px;
            }
            QComboBox::down-arrow {
                image: url(icons/down-arrow.png);
            }
        """)
        self.form_layout.addRow(QLabel('Produto:'), self.cmb_produto)

        # ComboBox para técnicos
        self.cmb_tecnico = QComboBox()
        self.cmb_tecnico.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #003d7a;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border-left: 1px solid #003d7a;
                padding-right: 5px;
            }
            QComboBox::down-arrow {
                image: url(icons/down-arrow.png);
            }
        """)
        self.form_layout.addRow(QLabel('Técnico:'), self.cmb_tecnico)

        # Campos de texto
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

        # Botão para retirar material
        btn_retirar = QPushButton('Retirar')
        btn_retirar.setStyleSheet("""
            QPushButton {
                background-color: #003d7a;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #00264d;
            }
        """)
        btn_retirar.clicked.connect(self.retirar_material)
        layout.addWidget(btn_retirar)

        # Botões para atualizar listas
        btn_atualizar_produtos = QPushButton('Atualizar Produtos')
        btn_atualizar_produtos.setStyleSheet("""
            QPushButton {
                background-color: #003d7a;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #00264d;
            }
        """)
        btn_atualizar_produtos.clicked.connect(self.update_products)
        layout.addWidget(btn_atualizar_produtos)

        btn_atualizar_tecnicos = QPushButton('Atualizar Técnicos')
        btn_atualizar_tecnicos.setStyleSheet("""
            QPushButton {
                background-color: #003d7a;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #00264d;
            }
        """)
        btn_atualizar_tecnicos.clicked.connect(self.update_tecnicos)
        layout.addWidget(btn_atualizar_tecnicos)

        self.setLayout(layout)

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
            QLineEdit {
                padding: 10px;
                border: 1px solid #003d7a;  /* Azul escuro */
                border-radius: 5px;
                background-color: #ffffff;  /* Branco */
                margin-bottom: 15px;
            }
        """)

    def set_date_validator(self):
        date_regex = QRegularExpression(r'\d{0,2}/?\d{0,2}/?\d{0,4}')
        date_validator = QRegularExpressionValidator(date_regex, self)
        self.txt_data.setValidator(date_validator)
        self.txt_data.textChanged.connect(self.format_date)

    def format_date(self):
        text = self.txt_data.text()
        text = text.replace('/', '')
        if len(text) > 2:
            text = f"{text[:2]}/{text[2:]}"
        if len(text) > 5:
            text = f"{text[:5]}/{text[5:]}"
        if len(text) > 10:
            text = text[:10]
        self.txt_data.setText(text)
        self.txt_data.setCursorPosition(len(text))

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

            produto_id = self.cmb_produto.currentData()
            tecnico_id = self.cmb_tecnico.currentData()
            local = self.txt_local.text().strip()
            ordem_servico = self.txt_ordem_servico.text().strip()
            patrimonio = self.txt_patrimonio.text().strip()

            if not produto_id or not tecnico_id or not local or not ordem_servico:
                QMessageBox.warning(self, 'Erro', 'Todos os campos obrigatórios devem ser preenchidos!')
                return

            data = datetime.now().date()

            session = Session()

            # Buscar o produto pelo ID
            try:
                produto = session.query(Material).filter_by(id=produto_id).one()
            except NoResultFound:
                QMessageBox.warning(self, 'Erro', 'Produto não encontrado!')
                return

            # Buscar o técnico pelo ID
            try:
                tecnico = session.query(Tecnico).filter_by(id=tecnico_id).one()
            except NoResultFound:
                QMessageBox.warning(self, 'Erro', 'Técnico não encontrado!')
                return

            if patrimonio and patrimonio != produto.patrimonio:
                QMessageBox.warning(self, 'Erro', 'Patrimônio informado não corresponde ao patrimônio registrado!')
                return

            if quantidade <= produto.quantidade:
                # Subtrai a quantidade do estoque total
                produto.quantidade -= quantidade

                # Cria o registro de retirada
                retirada = RetiradaMaterial(
                    codigo=ordem_servico,
                    ordem_servico=ordem_servico,
                    produto_id=produto.id,
                    tecnico_id=tecnico.id,
                    quantidade=quantidade,
                    data=data,
                    local=local,
                    patrimonio=patrimonio or None,
                    devolvido=False
                )
                session.add(retirada)
                session.commit()

                QMessageBox.information(self, 'Sucesso',
                                        f'{quantidade} unidades de {produto.nome} retiradas com sucesso! Patrimônio: {produto.patrimonio}')
                self.clear_fields()
            else:
                QMessageBox.warning(self, 'Erro', 'Quantidade solicitada maior do que a disponível!')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao retirar material: {e}')
        finally:
            if session:
                session.close()

    def clear_fields(self):
        self.cmb_produto.setCurrentIndex(-1)
        self.cmb_tecnico.setCurrentIndex(-1)
        self.txt_quantidade.clear()
        self.txt_data.clear()
        self.txt_local.clear()
        self.txt_ordem_servico.clear()
        self.txt_patrimonio.clear()

    def update_products(self):
        session = None
        try:
            session = Session()
            produtos = session.query(Material).all()

            # Limpa o combo box
            self.cmb_produto.clear()

            # Adiciona os produtos ao combo box
            for produto in produtos:
                self.cmb_produto.addItem(produto.nome, produto.id)

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao atualizar produtos: {e}')
        finally:
            if session:
                session.close()

    def update_tecnicos(self):
        session = None
        try:
            session = Session()
            tecnicos = session.query(Tecnico).all()

            # Limpa o combo box
            self.cmb_tecnico.clear()

            # Adiciona os técnicos ao combo box
            for tecnico in tecnicos:
                self.cmb_tecnico.addItem(tecnico.nome, tecnico.id)

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao atualizar técnicos: {e}')
        finally:
            if session:
                session.close()
