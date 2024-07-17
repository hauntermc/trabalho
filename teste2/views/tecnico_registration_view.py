from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel
from controllers.tecnico_controller import register_tecnico

class TecnicoRegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Registrar Técnico')
        self.setGeometry(200, 200, 400, 200)

        # Layout principal
        layout = QVBoxLayout()

        # Label e campo de entrada para Nome do Técnico
        label_nome = QLabel('Nome do Técnico')
        self.nome_input = QLineEdit(self)
        layout.addWidget(label_nome)
        layout.addWidget(self.nome_input)

        # Label e campo de entrada para Telefone
        label_telefone = QLabel('Telefone')
        self.telefone_input = QLineEdit(self)
        layout.addWidget(label_telefone)
        layout.addWidget(self.telefone_input)

        # Label e campo de entrada para Matrícula
        label_matricula = QLabel('Matrícula')
        self.matricula_input = QLineEdit(self)
        layout.addWidget(label_matricula)
        layout.addWidget(self.matricula_input)

        # Botão de registro
        registrar_button = QPushButton('Registrar', self)
        registrar_button.clicked.connect(self.registrar_tecnico)
        layout.addWidget(registrar_button)

        # Adicionando o layout principal ao widget
        self.setLayout(layout)

    def registrar_tecnico(self):
        nome = self.nome_input.text().strip()
        telefone = self.telefone_input.text().strip()
        matricula = self.matricula_input.text().strip()

        if not nome or not telefone or not matricula:
            QMessageBox.warning(self, 'Erro', 'Por favor, preencha todos os campos.')
            return

        try:
            # Chama a função do controller para registrar o técnico
            resultado = register_tecnico(nome, telefone, matricula)

            if resultado is True:
                QMessageBox.information(self, 'Sucesso', f'Técnico {nome} registrado com sucesso!')
                self.nome_input.clear()
                self.telefone_input.clear()
                self.matricula_input.clear()
            else:
                QMessageBox.critical(self, 'Erro', f'Erro ao registrar técnico {nome}. A matrícula já está em uso.')

        except ValueError as ve:
            QMessageBox.critical(self, 'Erro', str(ve))

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao registrar técnico {nome}. Detalhes: {str(e)}')

