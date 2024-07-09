from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_backend import engine  # Importe seu engine SQLAlchemy aqui
from produto_database import Produto, engine

class RegisterProductWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Registrar Produto')
        self.initUI()

    def initUI(self):
        label = QLabel('Informações do Produto', self)

        self.product_name_input = QLineEdit(self)
        self.product_name_input.setPlaceholderText('Nome do Produto')

        self.product_price_input = QLineEdit(self)
        self.product_price_input.setPlaceholderText('Preço do Produto')

        register_button = QPushButton('Registrar', self)
        register_button.clicked.connect(self.register_product)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.product_name_input)
        layout.addWidget(self.product_price_input)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def register_product(self):
        product_name = self.product_name_input.text()
        product_price_text = self.product_price_input.text()

        try:
            product_price = float(product_price_text)  # Converte para float
        except ValueError:
            QMessageBox.warning(self, 'Erro de Registro', 'Por favor, insira um preço válido.')
            return

        # Cria uma sessão do SQLAlchemy
        Session = sessionmaker(bind=engine)
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
