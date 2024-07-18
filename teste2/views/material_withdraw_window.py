from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from utils.db_utils import Session
from models import Material

class MaterialWithdrawWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Retirar Material')
        self.setGeometry(200, 200, 400, 200)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.lbl_quantidade = QLabel('Quantidade a Retirar:')
        self.txt_quantidade = QLineEdit()
        layout.addWidget(self.lbl_quantidade)
        layout.addWidget(self.txt_quantidade)

        btn_retirar = QPushButton('Retirar')
        btn_retirar.clicked.connect(self.retirar_material)
        layout.addWidget(btn_retirar)

        self.setLayout(layout)

    def retirar_material(self):
        try:
            quantidade = int(self.txt_quantidade.text())

            # Lógica para retirar a quantidade do banco de dados
            session = Session()
            produto_id = 1  # Defina o ID do produto a partir da seleção na janela principal
            produto = session.query(Material).filter_by(id=produto_id).first()

            if produto:
                if quantidade <= produto.quantidade:
                    produto.quantidade -= quantidade
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