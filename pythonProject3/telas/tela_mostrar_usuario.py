from PyQt5 import QtWidgets
from banco_de_dados import Usuario, session

class TelaMostrarUsuarios(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Usuários Cadastrados')
        self.setGeometry(100, 100, 400, 300)

        layout = QtWidgets.QVBoxLayout()

        self.texto = QtWidgets.QTextEdit()
        self.texto.setReadOnly(True)
        layout.addWidget(self.texto)

        self.setLayout(layout)
        self.mostrar_usuarios()

    def mostrar_usuarios(self):
        usuarios = session.query(Usuario).all()
        if usuarios:
            for usuario in usuarios:
                self.texto.append(f'ID: {usuario.id}, Nome: {usuario.nome}, Username: {usuario.username}')
        else:
            self.texto.append('Nenhum usuário encontrado.')
