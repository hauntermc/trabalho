from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox
from banco_de_dados import Tecnico, session

class TelaRegistroTecnico(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.nome_input = QLineEdit()
        self.matricula_input = QLineEdit()
        self.telefone_input = QLineEdit()

        layout.addRow('Nome:', self.nome_input)
        layout.addRow('Matrícula:', self.matricula_input)
        layout.addRow('Telefone:', self.telefone_input)

        self.save_button = QPushButton('Salvar')
        self.save_button.clicked.connect(self.salvar_tecnico)

        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.setWindowTitle('Registrar Técnico')

    def salvar_tecnico(self):
        nome = self.nome_input.text()
        matricula = self.matricula_input.text()
        telefone = self.telefone_input.text()

        if nome and matricula and telefone:
            try:
                novo_tecnico = Tecnico(nome=nome, matricula=matricula, telefone=telefone)
                session.add(novo_tecnico)
                session.commit()
                QMessageBox.information(self, 'Sucesso', 'Técnico registrado com sucesso!')
                self.nome_input.clear()
                self.matricula_input.clear()
                self.telefone_input.clear()
            except Exception as e:
                session.rollback()
                QMessageBox.critical(self, 'Erro', f'Erro ao registrar técnico: {e}')
        else:
            QMessageBox.warning(self, 'Erro', 'Todos os campos são obrigatórios.')
