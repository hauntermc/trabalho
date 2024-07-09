# register_tecnico_window.py
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from sqlalchemy.orm import sessionmaker
from tecnico_database import engine  # Importe seu engine SQLAlchemy aqui
from tecnico_database import Tecnico

class RegisterTecnicoWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Registrar Técnico')
        self.initUI()

    def initUI(self):
        label = QLabel('Informações do Técnico', self)

        self.tecnico_nome_input = QLineEdit(self)
        self.tecnico_nome_input.setPlaceholderText('Nome do Técnico')

        self.tecnico_telefone_input = QLineEdit(self)
        self.tecnico_telefone_input.setPlaceholderText('Telefone')

        self.tecnico_matricula_input = QLineEdit(self)
        self.tecnico_matricula_input.setPlaceholderText('Matrícula')

        register_button = QPushButton('Registrar', self)
        register_button.clicked.connect(self.register_tecnico)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.tecnico_nome_input)
        layout.addWidget(self.tecnico_telefone_input)
        layout.addWidget(self.tecnico_matricula_input)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def register_tecnico(self):
        tecnico_nome = self.tecnico_nome_input.text()
        tecnico_telefone = self.tecnico_telefone_input.text()
        tecnico_matricula = self.tecnico_matricula_input.text()

        if not tecnico_nome or not tecnico_telefone or not tecnico_matricula:
            QMessageBox.warning(self, 'Erro de Registro', 'Por favor, preencha todos os campos.')
            return

        # Cria uma sessão do SQLAlchemy
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Cria um novo objeto Tecnico com os dados inseridos
            new_tecnico = Tecnico(nome=tecnico_nome, telefone=tecnico_telefone, matricula=tecnico_matricula)

            # Adiciona o novo técnico à sessão
            session.add(new_tecnico)

            # Commit para salvar no banco de dados
            session.commit()

            QMessageBox.information(self, 'Registro de Técnico', 'Técnico registrado com sucesso!')
            self.accept()  # Fecha a janela após registrar o técnico
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao registrar o técnico: {str(e)}')
            session.rollback()  # Desfaz as alterações em caso de erro
        finally:
            session.close()  # Fecha a sessão do SQLAlchemy
