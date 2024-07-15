from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QKeyEvent
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from produto_database import Produto, Estoque, engine_produto
import datetime

class DateLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPlaceholderText("DD/MM/AAAA")
        self.setMaxLength(10)
        self.textChanged.connect(self.format_date)

    def format_date(self, text):
        if len(text) == 2 or len(text) == 5:
            if text[-1] != '/':
                self.setText(text + '/')
                self.setCursorPosition(len(text) + 1)

class RegisterProductWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Registrar Produto')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Labels e campos de entrada
        label_nome = QLabel('Nome: ')
        self.input_nome = QLineEdit()

        label_preco = QLabel('Preço: ')
        self.input_preco = QLineEdit()

        label_nota_fiscal = QLabel('Nota Fiscal: ')
        self.input_nota_fiscal = QLineEdit()

        label_quantidade = QLabel('Quantidade: ')
        self.input_quantidade = QLineEdit()

        label_data = QLabel('Data (DD/MM/AAAA): ')
        self.input_data = QLineEdit()

        # Adiciona os widgets ao layout vertical
        layout.addWidget(label_nome)
        layout.addWidget(self.input_nome)
        layout.addWidget(label_preco)
        layout.addWidget(self.input_preco)
        layout.addWidget(label_nota_fiscal)
        layout.addWidget(self.input_nota_fiscal)
        layout.addWidget(label_quantidade)
        layout.addWidget(self.input_quantidade)
        layout.addWidget(label_data)
        layout.addWidget(self.input_data)

        # Botão para confirmar o registro
        btn_confirmar = QPushButton('Registrar')
        btn_confirmar.clicked.connect(self.register_product)
        layout.addWidget(btn_confirmar)

        self.setLayout(layout)

    def register_product(self):
        # Obter os textos dos campos de entrada
        product_name = self.input_nome.text()
        product_price_text = self.input_preco.text()
        product_nota_fiscal = self.input_nota_fiscal.text()
        product_quantidade_text = self.input_quantidade.text()
        product_data_text = self.input_data.text()

        # Verifica se os campos estão preenchidos
        if not product_name or not product_price_text or not product_nota_fiscal or not product_quantidade_text or not product_data_text:
            QMessageBox.warning(self, 'Erro de Registro', 'Por favor, preencha todos os campos.')
            return

        try:
            # Converte o texto da data para um objeto datetime.date
            product_data = datetime.datetime.strptime(product_data_text, '%d/%m/%Y').date()
        except ValueError:
            QMessageBox.warning(self, 'Erro de Registro', 'Formato de data inválido. Use o formato DD/MM/AAAA.')
            return

        try:
            # Converte para float
            product_price = float(product_price_text)

            # Converte a quantidade para inteiro
            product_quantidade = int(product_quantidade_text)

            # Cria uma sessão do SQLAlchemy
            Session = sessionmaker(bind=engine_produto)
            session = Session()

            try:
                # Cria um novo objeto Produto com os dados inseridos
                new_product = Produto(nome=product_name, preco=product_price, nota_fiscal=product_nota_fiscal, data=product_data)

                # Adiciona o novo produto à sessão
                session.add(new_product)

                # Commit para salvar no banco de dados
                session.commit()

                # Verifica se o produto já existe no estoque
                estoque = session.query(Estoque).filter_by(produto_id=new_product.id).first()

                if estoque:
                    # Se existir, atualiza a quantidade
                    estoque.quantidade += product_quantidade
                else:
                    # Se não existir, cria uma nova entrada no estoque
                    novo_estoque = Estoque(produto_id=new_product.id, quantidade=product_quantidade)
                    session.add(novo_estoque)

                session.commit()

                QMessageBox.information(self, 'Registro de Produto', 'Produto registrado com sucesso!')
                self.accept()  # Fecha a janela após registrar o produto

            except SQLAlchemyError as e:
                QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao registrar o produto: {str(e)}')
                session.rollback()  # Desfaz as alterações em caso de erro
            finally:
                session.close()  # Fecha a sessão do SQLAlchemy

        except ValueError:
            QMessageBox.warning(self, 'Erro de Registro', 'Por favor, insira um preço válido.')
            return
