import os
import subprocess
import sys
from datetime import datetime

from banco_de_dados import session, Material, RetiradaMaterial, Tecnico  # Certifique-se de que o modelo `Tecnico` esteja importado
from PyQt5 import QtWidgets
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


class TelaRetirarMaterial(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Retirar Material')
        self.setGeometry(100, 100, 400, 300)

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Adicionar campos de entrada
        self.ordem_servico_input = QtWidgets.QLineEdit()
        self.nome_produto_input = QtWidgets.QComboBox()  # Substituímos QLineEdit por QComboBox
        self.quantidade_input = QtWidgets.QLineEdit()
        self.tecnico_nome_input = QtWidgets.QLineEdit()
        self.local_utilizacao_input = QtWidgets.QLineEdit()
        self.patrimonio_input = QtWidgets.QLineEdit()

        # Preencher o ComboBox com os nomes dos materiais disponíveis
        self.carregar_materiais()

        # Adicionar botões
        retirar_button = QtWidgets.QPushButton('Retirar')
        retirar_button.clicked.connect(self.retirar_material)

        layout.addWidget(QtWidgets.QLabel('Ordem de Serviço:'))
        layout.addWidget(self.ordem_servico_input)
        layout.addWidget(QtWidgets.QLabel('Nome do Produto:'))
        layout.addWidget(self.nome_produto_input)
        layout.addWidget(QtWidgets.QLabel('Quantidade:'))
        layout.addWidget(self.quantidade_input)
        layout.addWidget(QtWidgets.QLabel('Nome do Técnico:'))
        layout.addWidget(self.tecnico_nome_input)
        layout.addWidget(QtWidgets.QLabel('Local de Utilização:'))
        layout.addWidget(self.local_utilizacao_input)
        layout.addWidget(QtWidgets.QLabel('Patrimônio:'))
        layout.addWidget(self.patrimonio_input)
        layout.addWidget(retirar_button)

        self.setLayout(layout)

    def carregar_materiais(self):
        try:
            # Consultar os materiais disponíveis no banco de dados
            materiais = session.query(Material).all()
            # Adicionar os nomes dos materiais ao ComboBox
            for material in materiais:
                self.nome_produto_input.addItem(material.nome)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', f'Ocorreu um erro ao carregar os materiais: {str(e)}')

    def retirar_material(self):
        ordem_servico = self.ordem_servico_input.text()
        nome_produto = self.nome_produto_input.currentText()  # Obtém o texto selecionado no ComboBox
        tecnico_nome = self.tecnico_nome_input.text()
        local_utilizacao = self.local_utilizacao_input.text()
        patrimonio = self.patrimonio_input.text()
        quantidade = self.quantidade_input.text()

        # Verifica se a quantidade é válida
        if not quantidade.isdigit() or int(quantidade) <= 0:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'A quantidade deve ser um número maior que 0.')
            return

        try:
            self.registrar_retirada(ordem_servico, nome_produto, quantidade, tecnico_nome, local_utilizacao, patrimonio)
            QtWidgets.QMessageBox.information(self, 'Sucesso', 'Material retirado com sucesso!')

            hoje = datetime.now().strftime("%d/%m/%Y")
            # Dados para o PDF
            material_info = {
                'data_retirada': hoje,
                'nome_tecnico': tecnico_nome,
                'matricula_tecnico': '',
                'responsavel_controle': '',
                'matricula_responsavel': '',
                'local_destino': local_utilizacao,
                'numero_patrimonio': patrimonio,
                'tecnico_responsavel': tecnico_nome,
                'matricula_tecnico_responsavel': '',
                'supervisor_tecnico': '',
                'matricula_supervisor': '',
                'controle_materiais': '',
                'matricula_controle': '',
            }

            # Gerar o PDF
            pdf_filename = f"Requisicao_Material_{ordem_servico}.pdf"
            generate_form_pdf(pdf_filename, ordem_servico, material_info)

            QtWidgets.QMessageBox.information(self, 'PDF Gerado', f'O PDF foi gerado com sucesso: {pdf_filename}')

            # Abrir o PDF automaticamente
            self.abrir_pdf(pdf_filename)

        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', str(e))
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', f'Ocorreu um erro inesperado: {str(e)}')

    def registrar_retirada(self, ordem_servico, nome_produto, quantidade, tecnico_nome, local_utilizacao, patrimonio):
        try:
            # Verifique se o técnico está registrado
            tecnico = session.query(Tecnico).filter_by(nome=tecnico_nome).first()
            if not tecnico:
                raise ValueError("Técnico não registrado no banco de dados.")

            # Verifique se a ordem de serviço já foi usada
            retirada_existente = session.query(RetiradaMaterial).filter_by(ordem_servico=ordem_servico).first()
            if retirada_existente:
                raise ValueError("Já existe uma retirada com essa ordem de serviço.")

            # Verifique se o material está disponível
            material = session.query(Material).filter_by(nome=nome_produto, patrimonio=patrimonio).first()
            if material is None:
                raise ValueError("Material não encontrado")
            if material.quantidade < int(quantidade):
                raise ValueError("Quantidade solicitada maior que a disponível")

            # Crie a retirada
            retirada = RetiradaMaterial(
                ordem_servico=ordem_servico,
                nome_produto=nome_produto,
                quantidade=int(quantidade),
                tecnico_nome=tecnico_nome,
                local_utilizacao=local_utilizacao,
                patrimonio=patrimonio,
                material_id=material.id
            )

            # Atualize a quantidade de material
            material.quantidade -= int(quantidade)

            # Adicione a retirada ao banco de dados
            session.add(retirada)
            session.commit()

        except Exception as e:
            # Rollback em caso de erro
            session.rollback()
            raise e

    def abrir_pdf(self, pdf_filename):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(pdf_filename)
            elif os.name == 'posix':  # macOS ou Linux
                subprocess.run(['open', pdf_filename] if sys.platform == 'darwin' else ['xdg-open', pdf_filename])
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', f'Não foi possível abrir o PDF: {str(e)}')


def generate_form_pdf(filename, ordem_servico, material_info):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    cabecalho = ParagraphStyle(name='centered', alignment=1, fontSize=12)
    elements.append(Paragraph("Poder Judiciário do Estado do Rio de Janeiro - PJERJ", cabecalho))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Departamento de Segurança Eletrônica e de Telecomunicacoes - DETEL", cabecalho))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Serviço de Controle de Materiais", cabecalho))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("REQUISIÇÃO DE MATERIAIS", styles['Title']))
    elements.append(Spacer(1, 12))

    # Horizontal Table Data
    data = [
        ['Número da OS:', ordem_servico, 'Data de retirada:', material_info.get('data_retirada', '____________________')],
        ['Nome do técnico:', material_info.get('nome_tecnico', '____________________'), 'Matrícula:', material_info.get('matricula_tecnico', '____________________')],
        ['Resp. Controle:', material_info.get('responsavel_controle', '____________________'), 'Matrícula:', material_info.get('matricula_responsavel', '____________________')],
        ['Local de destino:', material_info.get('local_destino', '____________________'), 'Nº Patrimônio:', material_info.get('numero_patrimonio', '____________________')]
    ]

    table = Table(data, colWidths=[120, 150, 120, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Add space before signatures
    elements.append(Spacer(1, 350))

    # Signatures Section
    signatures_data = [
        ['Téc. Responsável:', material_info.get('tecnico_responsavel', '____________________'), 'Matrícula:', material_info.get('matricula_tecnico_responsavel', '____________________')],
        ['Supervisor Técnico:', material_info.get('supervisor_tecnico', '____________________'), 'Matrícula:', material_info.get('matricula_supervisor', '____________________')],
        ['Controle de Materiais:', material_info.get('controle_materiais', '____________________'), 'Matrícula:', material_info.get('matricula_controle', '____________________')],
    ]

    signatures_table = Table(signatures_data, colWidths=[140, 150, 80, 150])
    signatures_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(signatures_table)

    # Build PDF
    doc.build(elements)
