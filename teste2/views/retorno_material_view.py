import sys
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit, QApplication, \
    QFormLayout, QComboBox
from PyQt5.QtCore import QDate, pyqtSignal, Qt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Material, RetornoMaterial, RetiradaMaterial, Tecnico, engine

Session = sessionmaker(bind=engine)

class RetornoMaterialWindow(QWidget):
    material_returned = pyqtSignal()  # Signal to notify when the material is returned

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Retorno de Material")
        self.setGeometry(200, 200, 400, 300)
        self.initUI()

    def initUI(self):
        # Main Layout
        main_layout = QVBoxLayout()

        # Form Layout
        self.form_layout = QFormLayout()

        # Ordem de Serviço ComboBox
        self.ordem_servico_label = QLabel("Ordem de Serviço:")
        self.ordem_servico_input = QComboBox()
        self.form_layout.addRow(self.ordem_servico_label, self.ordem_servico_input)

        # Nome do Produto
        self.produto_label = QLabel("Nome do Produto:")
        self.produto_input = QLineEdit()
        self.form_layout.addRow(self.produto_label, self.produto_input)

        # Nome do Técnico
        self.tecnico_label = QLabel("Nome do Técnico:")
        self.tecnico_input = QLineEdit()
        self.form_layout.addRow(self.tecnico_label, self.tecnico_input)

        # Quantidade
        self.quantidade_label = QLabel("Quantidade:")
        self.quantidade_input = QLineEdit()
        self.form_layout.addRow(self.quantidade_label, self.quantidade_input)

        # Data de Retorno
        self.data_retorno_label = QLabel("Data de Retorno:")
        self.data_retorno_input = QDateEdit()
        self.data_retorno_input.setDate(QDate.currentDate())
        self.form_layout.addRow(self.data_retorno_label, self.data_retorno_input)

        # Patrimônio (opcional)
        self.patrimonio_label = QLabel("Patrimônio (opcional):")
        self.patrimonio_input = QLineEdit()
        self.form_layout.addRow(self.patrimonio_label, self.patrimonio_input)

        # Submit Button
        self.submit_button = QPushButton("Registrar Retorno")
        self.submit_button.clicked.connect(self.registrar_retorno)

        # Update Button
        self.update_button = QPushButton("Atualizar")
        self.update_button.clicked.connect(self.update_ordem_servico)

        # Add form layout to main layout
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(self.submit_button, alignment=Qt.AlignBottom)
        main_layout.addWidget(self.update_button, alignment=Qt.AlignBottom)

        self.setLayout(main_layout)

        # Style the interface
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;  /* Light Blue */
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #003d7a;  /* Dark Blue */
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit, QDateEdit, QComboBox {
                padding: 10px;
                border: 1px solid #003d7a;  /* Dark Blue */
                border-radius: 5px;
                background-color: #ffffff;  /* White */
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #003d7a;  /* Dark Blue */
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #00264d;  /* Even Darker Blue */
            }
        """)

        # Preencher o ComboBox de Ordem de Serviço
        self.update_ordem_servico()

    def update_ordem_servico(self):
        session = None
        try:
            session = Session()
            # Consulta para obter as ordens de serviço que ainda não foram retornadas
            ordens_servico = session.query(RetiradaMaterial).filter_by(devolvido=False).all()

            # Limpa o combo box
            self.ordem_servico_input.clear()

            # Adiciona as ordens de serviço ao combo box
            for ordem in ordens_servico:
                self.ordem_servico_input.addItem(ordem.ordem_servico, ordem.id)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar ordens de serviço: {e}")
        finally:
            if session:
                session.close()

    def registrar_retorno(self):
        ordem_servico = self.ordem_servico_input.currentData()
        produto_nome = self.produto_input.text().strip()
        tecnico_nome = self.tecnico_input.text().strip()
        quantidade_text = self.quantidade_input.text().strip()
        data_retorno = self.data_retorno_input.date().toPyDate()
        patrimonio = self.patrimonio_input.text().strip()

        if ordem_servico is None or not produto_nome or not tecnico_nome or not quantidade_text:
            QMessageBox.warning(self, "Erro", "Todos os campos obrigatórios devem ser preenchidos.")
            return

        try:
            quantidade = int(quantidade_text)
        except ValueError:
            QMessageBox.warning(self, "Erro", "Quantidade deve ser um número inteiro.")
            return

        session = Session()

        try:
            produto = session.query(Material).filter_by(nome=produto_nome).first()
            if produto is None:
                QMessageBox.warning(self, "Erro", "Produto não encontrado.")
                return

            tecnico = session.query(Tecnico).filter_by(nome=tecnico_nome).first()
            if tecnico is None:
                QMessageBox.warning(self, "Erro", "Técnico não encontrado.")
                return

            retirada = session.query(RetiradaMaterial).filter_by(
                id=ordem_servico,
                produto_id=produto.id,
                tecnico_id=tecnico.id
            ).first()

            if retirada is None:
                QMessageBox.warning(self, "Erro",
                                    "Não há registro de retirada com esta ordem de serviço para este produto e técnico.")
                return

            if quantidade > retirada.quantidade:
                QMessageBox.warning(self, "Erro", "Quantidade de retorno não pode exceder a quantidade retirada.")
                return

            retorno_existente = session.query(RetornoMaterial).filter_by(
                ordem_servico=ordem_servico,
                produto_id=produto.id,
                tecnico_id=tecnico.id
            ).first()

            if retorno_existente:
                QMessageBox.warning(self, "Erro", "O material já foi retornado anteriormente.")
                return

            # Atualizar ou adicionar material com patrimônio
            if patrimonio:
                material_existente = session.query(Material).filter_by(patrimonio=patrimonio).first()
                if material_existente:
                    material_existente.quantidade += quantidade
                else:
                    novo_material = Material(
                        nome=produto.nome,
                        preco=produto.preco,  # Use o preço do produto original
                        quantidade=quantidade,
                        patrimonio=patrimonio,
                        nota_fiscal=""  # Atualize conforme necessário
                    )
                    session.add(novo_material)
            else:
                produto.quantidade += quantidade

            # Registrar o retorno
            retorno = RetornoMaterial(
                ordem_servico=ordem_servico,
                produto_id=produto.id,
                tecnico_id=tecnico.id,
                quantidade=quantidade,
                data_retorno=data_retorno,
                data=datetime.utcnow().date()
            )
            session.add(retorno)

            # Atualizar a retirada
            retirada.quantidade -= quantidade
            if retirada.quantidade == 0:
                retirada.devolvido = True

            session.commit()

            QMessageBox.information(self, "Sucesso", "Retorno registrado com sucesso.")
            self.material_returned.emit()  # Emitir sinal após sucesso

            # Limpar campos
            self.produto_input.clear()
            self.tecnico_input.clear()
            self.quantidade_input.clear()
            self.patrimonio_input.clear()
            self.data_retorno_input.setDate(QDate.currentDate())
            self.update_ordem_servico()

        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Erro", f"Erro ao registrar retorno: {e}")

        finally:
            session.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RetornoMaterialWindow()
    window.show()
    sys.exit(app.exec_())
