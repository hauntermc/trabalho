from PyQt5 import QtWidgets
from banco_de_dados import session, Material, RetiradaMaterial

class TelaRetornoMaterial(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Retorno de Material')
        self.setGeometry(100, 100, 400, 300)

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Adicionar campos de entrada
        self.ordem_servico_input = QtWidgets.QLineEdit()
        self.nome_produto_input = QtWidgets.QLineEdit()
        self.tecnico_nome_input = QtWidgets.QLineEdit()
        self.quantidade_input = QtWidgets.QLineEdit()
        self.patrimonio_input = QtWidgets.QLineEdit()

        # Adicionar botões
        retornar_button = QtWidgets.QPushButton('Retornar')
        retornar_button.clicked.connect(self.retornar_material)

        layout.addWidget(QtWidgets.QLabel('Ordem de Serviço:'))
        layout.addWidget(self.ordem_servico_input)
        layout.addWidget(QtWidgets.QLabel('Nome do Produto:'))
        layout.addWidget(self.nome_produto_input)
        layout.addWidget(QtWidgets.QLabel('Nome do Técnico:'))
        layout.addWidget(self.tecnico_nome_input)
        layout.addWidget(QtWidgets.QLabel('Quantidade:'))
        layout.addWidget(self.quantidade_input)
        layout.addWidget(QtWidgets.QLabel('Patrimônio:'))
        layout.addWidget(self.patrimonio_input)
        layout.addWidget(retornar_button)

        self.setLayout(layout)

    def retornar_material(self):
        ordem_servico = self.ordem_servico_input.text()
        nome_produto = self.nome_produto_input.text()
        tecnico_nome = self.tecnico_nome_input.text()
        patrimonio = self.patrimonio_input.text()
        quantidade = self.quantidade_input.text()
        try:
            self.registrar_retorno(ordem_servico, nome_produto, tecnico_nome, quantidade, patrimonio)
            QtWidgets.QMessageBox.information(self, 'Sucesso', 'Material retornado com sucesso!')
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', str(e))

    def registrar_retorno(self, ordem_servico, nome_produto, tecnico_nome, quantidade, patrimonio):
        # Verifique se o material está registrado como retirado
        retirada = session.query(RetiradaMaterial).filter_by(
            ordem_servico=ordem_servico,
            nome_produto=nome_produto,
            quantidade=quantidade,
            tecnico_nome=tecnico_nome,
            patrimonio=patrimonio
        ).first()

        if retirada is None:
            raise ValueError("Retirada não encontrada")

        # Recupere o material
        material = session.query(Material).filter_by(nome=nome_produto, patrimonio=patrimonio).first()
        if material is None:
            raise ValueError("Material não encontrado")

        # Interpretar a quantidade
        if quantidade.startswith('DIS'):
            # Lógica para tratar quantidades no formato DIS
            if material.quantidade_textual:
                # Atualize a quantidade textual existente
                material.quantidade_textual = quantidade
            else:
                # Defina a quantidade textual se não existir
                material.quantidade_textual = quantidade
        else:
            try:
                quantidade_int = int(quantidade)  # Verifique se a quantidade é um número válido
                material.quantidade += quantidade_int
            except ValueError:
                raise ValueError("Quantidade deve ser um número inteiro")

        # Remova a retirada do banco de dados
        session.delete(retirada)
        session.commit()
