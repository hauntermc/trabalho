from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QApplication,
                             QFileDialog, QMessageBox, QInputDialog, QLabel, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
import fitz  # PyMuPDF
import os
from sqlalchemy.orm import Session

from models import Material, Tecnico, RetiradaMaterial
from utils.pdf_utils import generate_form_pdf
from utils.db_utils import Session


class PDFViewer(QWidget):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Visualizador de PDF')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Label para exibir o PDF
        self.pdf_label = QLabel(self)
        layout.addWidget(self.pdf_label)

        # Botão de Impressão
        self.print_button = QPushButton('Imprimir PDF', self)
        self.print_button.clicked.connect(self.print_pdf)
        layout.addWidget(self.print_button)

        self.setLayout(layout)

        self.show_pdf(file_path)

    def show_pdf(self, file_path):
        # Verifica se o arquivo existe
        if not os.path.exists(file_path):
            QMessageBox.critical(self, 'Erro', 'O arquivo PDF não foi encontrado.')
            return

        # Abre o PDF e exibe a primeira página
        pdf_document = fitz.open(file_path)
        if pdf_document.page_count > 0:
            page = pdf_document.load_page(0)  # Carrega a primeira página
            pix = page.get_pixmap()
            img_path = file_path + '.png'
            pix.save(img_path)

            pixmap = QPixmap(img_path)
            self.pdf_label.setPixmap(pixmap)
            os.remove(img_path)  # Remove a imagem temporária
        else:
            QMessageBox.warning(self, 'Erro', 'O PDF está vazio ou não contém páginas.')

    def print_pdf(self):
        # Cria um objeto QPrinter
        printer = QPrinter()
        printer.setPageSize(QPrinter.A4)
        printer.setOrientation(QPrinter.Portrait)

        # Abre o diálogo de impressão
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec_() == QPrintDialog.Accepted:
            # Configure a impressão
            pdf_document = fitz.open(self.file_path)
            if pdf_document.page_count > 0:
                page = pdf_document.load_page(0)  # Carrega a primeira página
                pdf_document.save(printer, deflate=False, incremental=True)
            else:
                QMessageBox.warning(self, 'Erro', 'O PDF está vazio ou não contém páginas.')


class AfterLoginScreen(QWidget):
    close_all_windows_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tela Principal')
        self.setGeometry(100, 100, 800, 600)

        # Configura o estilo
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;  /* Azul claro para o fundo */
                color: #333;  /* Cor do texto */
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #87cefa;  /* Azul claro para os botões */
                border: 1px solid #1e90ff;  /* Azul mais escuro para a borda */
                border-radius: 8px;
                padding: 10px 15px;  /* Ajustar preenchimento */
                font-size: 16px;  /* Ajustar tamanho da fonte */
                min-width: 150px;  /* Largura mínima */
                outline: none;  /* Remove a borda de foco padrão */
            }
            QPushButton:hover {
                background-color: #1e90ff;  /* Azul mais escuro ao passar o mouse */
                color: white;
            }
            QPushButton:pressed {
                background-color: #4682b4;  /* Azul mais escuro ao pressionar */
            }
            QPushButton:focus {
                outline: none;  /* Remove a borda de foco ao clicar */
            }
        """)

        # Criar botões
        self.btn_registrar_produto = QPushButton('Registrar Produto')
        self.btn_registrar_fornecedor = QPushButton('Registrar Fornecedor')
        self.btn_registrar_tecnico = QPushButton('Registrar Técnico')
        self.btn_retirar_material = QPushButton('Retirar Material')
        self.btn_retorno_material = QPushButton('Retorno de Material')
        self.btn_mostrar_produto = QPushButton('Mostrar Produtos')
        self.btn_mostrar_tecnico = QPushButton('Mostrar Técnicos')
        self.btn_mostrar_produtos_retirados = QPushButton('Mostrar Produtos Retirados')
        self.btn_mostrar_estoque = QPushButton('Mostrar Estoque Total')
        self.btn_adicionar_usuario = QPushButton('Adicionar Novo Usuário')
        self.btn_gerar_pdf = QPushButton('Gerar PDF')
        self.btn_procurar_pdf = QPushButton('Procurar PDF')

        self.btn_procurar_pdf.clicked.connect(self.procurar_pdf)
        self.btn_gerar_pdf.clicked.connect(self.gerar_pdf)

        # Adicionar ícone ao botão de logout com redimensionamento da imagem
        self.btn_logout = QPushButton()
        self.btn_logout.setObjectName('logoutButton')
        self.btn_logout.setStyleSheet("""
            QPushButton#logoutButton {
                border: none;  /* Remove a borda do botão */
                background: none;  /* Define fundo como nenhum para usar a imagem programaticamente */
                width: 50px;  /* Largura do botão */
                height: 50px;  /* Altura do botão */
                border-radius: 25px;  /* Tornar o botão redondo */
            }
        """)

        # Redimensionar e aplicar a imagem ao botão de logout
        self.set_logout_button_icon('C:/Users/Detel/Desktop/pngwing.com.png', 50, 50)

        # Layout dos botões
        button_layout1 = QVBoxLayout()
        button_layout1.addWidget(self.btn_registrar_produto)
        button_layout1.addWidget(self.btn_registrar_fornecedor)
        button_layout1.addWidget(self.btn_registrar_tecnico)
        button_layout1.addWidget(self.btn_retirar_material)
        button_layout1.addWidget(self.btn_retorno_material)

        button_layout2 = QVBoxLayout()
        button_layout2.addWidget(self.btn_mostrar_produto)
        button_layout2.addWidget(self.btn_mostrar_tecnico)
        button_layout2.addWidget(self.btn_mostrar_produtos_retirados)
        button_layout2.addWidget(self.btn_mostrar_estoque)
        button_layout2.addWidget(self.btn_adicionar_usuario)
        button_layout2.addWidget(self.btn_gerar_pdf)
        button_layout2.addWidget(self.btn_procurar_pdf)

        #Criar um label para a imagem
        self.image_label = QLabel()
        self.set_image('C:/Users/Detel/Desktop/logo-pjerj-preto.png') #Caminho da imagem


        # Layout principal
        main_layout = QGridLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  # Ajustar margens
        main_layout.setHorizontalSpacing(15)  # Ajustar espaçamento horizontal
        main_layout.setVerticalSpacing(15)  # Ajustar espaçamento vertical

        main_layout.addLayout(button_layout1, 0, 0)  # Coluna 0
        main_layout.addLayout(button_layout2, 0, 1)  # Coluna 1

        # Adicionar o botão de logout na parte inferior direita
        logout_layout = QHBoxLayout()
        logout_layout.addStretch()  # Adicionar espaçador flexível à esquerda
        logout_layout.addWidget(self.btn_logout)
        main_layout.addLayout(logout_layout, 1, 0, 1, 2, Qt.AlignRight)

        self.setLayout(main_layout)

        # Mostrar em tela cheia
        self.showFullScreen()

    def set_logout_button_icon(self, image_path, width, height):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        icon = QIcon(pixmap)
        self.btn_logout.setIcon(icon)
        self.btn_logout.setIconSize(pixmap.size())

    def closeEvent(self, event):
        self.close_all_windows_signal.emit()  # Emitir o sinal ao fechar a janela
        super().closeEvent(event)

    def habilitar_botao_adicionar_usuario(self):
        self.btn_adicionar_usuario.setEnabled(True)

    def desabilitar_botao_adicionar_usuario(self):
        self.btn_adicionar_usuario.setEnabled(False)

    def gerar_pdf(self):
        ordem_servico, ok = QInputDialog.getText(self, 'Ordem de Serviço', 'Digite a ordem de serviço:')
        if ok and ordem_servico:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Salvar PDF", f"{ordem_servico}.pdf",
                                                       "PDF Files (*.pdf);;All Files (*)",
                                                       options=options)

            if file_name:
                try:
                    # Obtém uma sessão do banco de dados
                    session = Session()

                    # Recupera a informação da retirada com base na ordem de serviço
                    retirada = session.query(RetiradaMaterial).filter_by(ordem_servico=ordem_servico).first()

                    if retirada:
                        material_info = {
                            'data_retirada': retirada.data.strftime('%d/%m/%Y'),
                            'nome_tecnico': retirada.tecnico.nome,
                            'matricula_tecnico': retirada.tecnico.matricula,
                            'local_destino': retirada.local,
                            'numero_patrimonio': retirada.patrimonio
                        }

                        # Gera o PDF
                        generate_form_pdf(file_name, ordem_servico, material_info)
                        QMessageBox.information(self, 'PDF Gerado', 'O PDF foi gerado com sucesso!')
                    else:
                        QMessageBox.warning(self, 'Retirada Não Encontrada',
                                            'Nenhuma retirada encontrada para a ordem de serviço fornecida.')

                except Exception as e:
                    QMessageBox.critical(self, 'Erro ao Gerar PDF', f'Ocorreu um erro ao gerar o PDF: {e}')
            else:
                QMessageBox.warning(self, 'Nome do Arquivo Inválido', 'O nome do arquivo não pode ser vazio.')
        else:
            QMessageBox.warning(self, 'Ordem de Serviço Inválida', 'Ordem de serviço não fornecida.')

    def procurar_pdf(self):
        # Adiciona um diálogo para obter a ordem de serviço
        ordem_servico, ok = QInputDialog.getText(self, 'Ordem de Serviço', 'Digite a ordem de serviço:')
        if ok and ordem_servico:
            # Verifica se o arquivo PDF existe com o nome da ordem de serviço
            self.pdf_path = f"{ordem_servico}.pdf"  # Defina o diretório onde os PDFs estão armazenados
            if os.path.exists(self.pdf_path):
                # Cria uma janela para mostrar o PDF
                self.pdf_viewer = PDFViewer(self.pdf_path)
                self.pdf_viewer.show()
            else:
                QMessageBox.warning(self, 'Arquivo Não Encontrado',
                                    'Nenhum arquivo PDF encontrado para a ordem de serviço fornecida.')

    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)