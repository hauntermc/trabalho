from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from produto_database import Produto, engine_produto

class RegisterProductWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Registrar Produto')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Labels e campos de entrada
        label_nome = QLabel('Nome:')
        self.input_nome = QLineEdit()

        label_preco = QLabel('Preço:')
        self.input_preco = QLineEdit()

        # Adiciona os widgets ao layout vertical
        layout.addWidget(label_nome)
        layout.addWidget(self.input_nome)
        layout.addWidget(label_preco)
        layout.addWidget(self.input_preco)

        # Botão para confirmar o registro
        btn_confirmar = QPushButton('Registrar')
        btn_confirmar.clicked.connect(self.register_product)
        layout.addWidget(btn_confirmar)

        self.setLayout(layout)

    def register_product(self):
        product_name = self.input_nome.text()
        product_price_text = self.input_preco.text()

        try:
            product_price = float(product_price_text)  # Converte para float
        except ValueError:
            QMessageBox.warning(self, 'Erro de Registro', 'Por favor, insira um preço válido.')
            return

        # Cria uma sessão do SQLAlchemy
        Session = sessionmaker(bind=engine_produto)
        session = Session()

        try:
            # Cria um novo objeto Produto com os dados inseridos
            new_product = Produto(nome=product_name, preco=product_price)

            # Adiciona o novo produto à sessão
            session.add(new_product)

            # Commit para salvar no banco de dados
            session.commit()

            QMessageBox.information(self, 'Registro de Produto', 'Produto registrado com sucesso!')
            self.accept()  # Fecha a janela após registrar o produto
        except SQLAlchemyError as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao registrar o produto: {str(e)}')
            session.rollback()  # Desfaz as alterações em caso de erro
        finally:
            session.close()  # Fecha a sessão do SQLAlchemy
