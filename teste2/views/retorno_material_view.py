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

        # Main Layout
        main_layout = QVBoxLayout()

        # Form Layout
        self.form_layout = QFormLayout()

        # Ordem de Serviço
        self.ordem_servico_label = QLabel("Ordem de Serviço:")
        self.ordem_servico_input = QLineEdit()
        self.form_layout.addRow(self.ordem_servico_label, self.ordem_servico_input)

        # Nome do Produto
        self.produto_label = QLabel("Nome do Produto:")
        self.cmb_produto = QComboBox()
        self.form_layout.addRow(self.produto_label, self.cmb_produto)

        # Seleção de Técnico
        self.tecnico_label = QLabel("Selecionar Técnico:")
        self.cmb_tecnico = QComboBox()
        self.form_layout.addRow(self.tecnico_label, self.cmb_tecnico)

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

        # Add form layout to main layout
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(self.submit_button, alignment=Qt.AlignBottom)

        self.setLayout(main_layout)

        # Populate ComboBoxes
        self.populate_tecnicos()
        self.populate_produtos()

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
            QLineEdit, QComboBox, QDateEdit {
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

    def populate_tecnicos(self):
        session = Session()
        try:
            self.cmb_tecnico.clear()
            self.cmb_tecnico.addItem("Selecione um técnico")  # Optional default item

            tecnicos = session.query(Tecnico).all()
            for tecnico in tecnicos:
                self.cmb_tecnico.addItem(f"{tecnico.nome} (Matrícula: {tecnico.matricula})", userData=tecnico.id)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar técnicos: {e}")
        finally:
            session.close()

    def populate_produtos(self):
        session = Session()
        try:
            self.cmb_produto.clear()
            self.cmb_produto.addItem("Selecione um produto")  # Optional default item

            # Filtrar produtos com base nas retiradas que ainda não foram retornadas
            retiradas_nao_retorno = session.query(RetiradaMaterial).filter_by(devolvido=False).all()
            produto_ids = {retirada.produto_id for retirada in retiradas_nao_retorno}
            produtos = session.query(Material).filter(Material.id.in_(produto_ids)).all()

            for produto in produtos:
                quantidade_disponivel = sum(retirada.quantidade for retirada in retiradas_nao_retorno if retirada.produto_id == produto.id)
                self.cmb_produto.addItem(f"{produto.nome} (Quantidade: {quantidade_disponivel})", userData=produto.id)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar produtos: {e}")
        finally:
            session.close()

    def registrar_retorno(self):
        ordem_servico = self.ordem_servico_input.text()
        produto_id = self.cmb_produto.currentData()
        tecnico_id = self.cmb_tecnico.currentData()
        quantidade = self.quantidade_input.text()
        data_retorno = self.data_retorno_input.date().toPyDate()
        patrimonio = self.patrimonio_input.text()

        if not ordem_servico or produto_id is None or tecnico_id is None or not quantidade:
            QMessageBox.warning(self, "Erro", "Todos os campos obrigatórios devem ser preenchidos.")
            return

        try:
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

            retirada = session.query(RetiradaMaterial).filter_by(
                ordem_servico=ordem_servico,
                produto_id=produto.id,
                tecnico_id=tecnico_id
            ).first()

            if retirada is None:
                QMessageBox.warning(self, "Erro",
                                    "Não há registro de retirada com esta ordem de serviço para este produto e técnico.")
                return

            retorno_existente = session.query(RetornoMaterial).filter_by(
                ordem_servico=ordem_servico,
                produto_id=produto.id,
                tecnico_id=tecnico_id
            ).first()

            if retorno_existente:
                QMessageBox.warning(self, "Erro", "O material já foi retornado anteriormente.")
                return

            if patrimonio:
                material_existente = session.query(Material).filter_by(patrimonio=patrimonio).first()
                if material_existente:
                    material_existente.quantidade += quantidade
                else:
                    novo_material = Material(
                        nome=produto.nome,
                        preco=0.0,
                        quantidade=quantidade,
                        patrimonio=patrimonio,
                        nota_fiscal=""  # Atualize conforme necessário
                    )
                    session.add(novo_material)
                session.commit()

            retorno = RetornoMaterial(
                ordem_servico=ordem_servico,
                produto_id=produto.id,
                tecnico_id=tecnico_id,
                quantidade=quantidade,
                data_retorno=data_retorno,
                data=datetime.utcnow().date()
            )
            session.add(retorno)

            produto.quantidade += quantidade
            retirada.devolvido = True
            session.commit()

            QMessageBox.information(self, "Sucesso", "Retorno registrado com sucesso.")
            self.material_returned.emit()

            # Clear fields
            self.ordem_servico_input.clear()
            self.cmb_produto.setCurrentIndex(0)
            self.cmb_tecnico.setCurrentIndex(0)
            self.quantidade_input.clear()
            self.patrimonio_input.clear()
            self.data_retorno_input.setDate(QDate.currentDate())

            self.populate_produtos()
            self.populate_tecnicos()

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
