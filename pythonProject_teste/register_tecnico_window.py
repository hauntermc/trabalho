# register_tecnico_window.py
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from sqlalchemy.orm import sessionmaker
from tecnico_database import engine_tecnico
from tecnico_database import Tecnico

class RegisterTecnicoWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Registrar Técnico')
        self.initUI()

    def initUI(self):
        self.label_nome = QLabel('Nome:', self)
        self.tecnico_nome_input = QLineEdit()
        #self.tecnico_nome_input.setPlaceholderText('Nome do Técnico')

        self.label_telefone = QLabel('Telefone:', self)
        self.tecnico_telefone_input = QLineEdit()
        #self.tecnico_telefone_input.setPlaceholderText('Telefone do Técnico')

        self.label_matricula = QLabel('Matrícula:', self)
        self.tecnico_matricula_input = QLineEdit()
        #self.tecnico_matricula_input.setPlaceholderText('Matrícula do Técnico')

        register_button = QPushButton('Registrar', self)
        register_button.clicked.connect(self.register_tecnico)

        layout = QVBoxLayout()
        layout.addWidget(self.label_nome)
        layout.addWidget(self.tecnico_nome_input)
        layout.addWidget(self.label_telefone)
        layout.addWidget(self.tecnico_telefone_input)
        layout.addWidget(self.label_matricula)
        layout.addWidget(self.tecnico_matricula_input)
        layout.addWidget(register_button)

        self.setLayout(layout)

        # Definindo a ordem de tabulação
        self.setTabOrder(self.tecnico_nome_input, self.tecnico_telefone_input)
        self.setTabOrder(self.tecnico_telefone_input, self.tecnico_matricula_input)
        self.setTabOrder(self.tecnico_matricula_input, register_button)

    def register_tecnico(self):
        tecnico_nome = self.tecnico_nome_input.text()
        tecnico_telefone = self.tecnico_telefone_input.text()
        tecnico_matricula = self.tecnico_matricula_input.text()

        if not tecnico_nome or not tecnico_telefone or not tecnico_matricula:
            QMessageBox.warning(self, 'Erro de Registro', 'Por favor, preencha todos os campos.')
            return

        Session = sessionmaker(bind=engine_tecnico)
        session = Session()

        try:
            new_tecnico = Tecnico(nome=tecnico_nome, telefone=tecnico_telefone, matricula=tecnico_matricula)
            session.add(new_tecnico)
            session.commit()

            QMessageBox.information(self, 'Registro de Técnico', 'Técnico registrado com sucesso!')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao registrar o técnico: {str(e)}')
            session.rollback()
        finally:
            session.close()
