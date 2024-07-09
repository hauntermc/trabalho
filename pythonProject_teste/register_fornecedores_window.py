from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from fornecedores_database import engine  # Importe seu engine SQLAlchemy aqui
from fornecedores_database import Fornecedor

class RegisterFornecedorWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Registrar Fornecedor')
        self.initUI()

    def initUI(self):
        label = QLabel('Informações do Fornecedor', self)

        self.fornecedor_nome_input = QLineEdit(self)
        self.fornecedor_nome_input.setPlaceholderText('Nome do Fornecedor')

        self.fornecedor_cnpj_input = QLineEdit(self)
        self.fornecedor_cnpj_input.setPlaceholderText('CNPJ do Fornecedor')

        register_button = QPushButton('Registrar', self)
        register_button.clicked.connect(self.register_fornecedor)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.fornecedor_nome_input)
        layout.addWidget(self.fornecedor_cnpj_input)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def register_fornecedor(self):
        fornecedor_nome = self.fornecedor_nome_input.text()
        fornecedor_cnpj = self.fornecedor_cnpj_input.text()

        if not fornecedor_nome or not fornecedor_cnpj:
            QMessageBox.warning(self, 'Erro de Registro', 'Por favor, preencha todos os campos.')
            return

        # Cria uma sessão do SQLAlchemy
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Cria um novo objeto Fornecedor com os dados inseridos
            new_fornecedor = Fornecedor(nome=fornecedor_nome, cnpj=fornecedor_cnpj)

            # Adiciona o novo fornecedor à sessão
            session.add(new_fornecedor)

            # Commit para salvar no banco de dados
            session.commit()

            QMessageBox.information(self, 'Registro de Fornecedor', 'Fornecedor registrado com sucesso!')
            self.accept()  # Fecha a janela após registrar o fornecedor
        except IntegrityError:
            session.rollback()
            QMessageBox.warning(self, 'Erro de Registro', 'Fornecedor já existe.')
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao registrar o fornecedor: {str(e)}')
        finally:
            session.close()  # Fecha a sessão do SQLAlchemy
