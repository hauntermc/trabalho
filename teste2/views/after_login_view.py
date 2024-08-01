from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QApplication,
                             QFileDialog, QMessageBox, QInputDialog, QLabel, QTabWidget)
from PyQt5.QtCore import Qt, pyqtSignal, QMarginsF
from PyQt5.QtGui import QPixmap, QIcon, QPdfWriter, QPageSize, QPainter, QImage
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import os
import logging
import fitz
from sqlalchemy.orm import Session

from models import Material, Tecnico, RetiradaMaterial
from utils.pdf_utils import generate_form_pdf
from utils.db_utils import Session
from views.showtecnico_view import ShowTecnicoWindow

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)


class PDFViewer(QWidget):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.setWindowTitle('Visualizador de PDF')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.pdf_label = QLabel(self)
        layout.addWidget(self.pdf_label)

        self.print_button = QPushButton('Imprimir PDF', self)
        self.print_button.clicked.connect(self.print_pdf)
        layout.addWidget(self.print_button)

        self.setLayout(layout)
        self.show_pdf(file_path)

    def show_pdf(self, file_path):
        if not os.path.exists(file_path):
            QMessageBox.critical(self, 'Erro', 'O arquivo PDF não foi encontrado.')
            return

        pdf_document = fitz.open(file_path)
        if pdf_document.page_count > 0:
            page = pdf_document.load_page(0)
            pix = page.get_pixmap()
            img_path = file_path + '.png'
            pix.save(img_path)

            pixmap = QPixmap(img_path)
            self.pdf_label.setPixmap(pixmap)
            os.remove(img_path)
        else:
            QMessageBox.warning(self, 'Erro', 'O PDF está vazio ou não contém páginas.')

    def print_pdf(self):
        printer = QPrinter()
        printer.setPageSize(QPrinter.A4)
        printer.setOrientation(QPrinter.Portrait)

        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec_() == QPrintDialog.Accepted:
            try:
                pdf_document = fitz.open(self.file_path)
                if pdf_document.page_count > 0:
                    pdf_writer = QPdfWriter(printer)
                    pdf_writer.setResolution(300)
                    pdf_writer.setPageSize(QPageSize.A4)
                    pdf_writer.setPageMargins(QMarginsF(15, 15, 15, 15))

                    painter = QPainter(pdf_writer)
                    for page_num in range(pdf_document.page_count):
                        page = pdf_document.load_page(page_num)
                        pix = page.get_pixmap()
                        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
                        rect = painter.viewport()
                        size = img.size()
                        size.scale(rect.size(), Qt.KeepAspectRatio)
                        painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
                        painter.setWindow(img.rect())
                        painter.drawImage(0, 0, img)
                        if page_num < pdf_document.page_count - 1:
                            pdf_writer.newPage()
                    painter.end()
                else:
                    QMessageBox.warning(self, 'Erro', 'O PDF está vazio ou não contém páginas.')
            except Exception as e:
                QMessageBox.critical(self, 'Erro ao Imprimir', f'Ocorreu um erro ao imprimir o PDF: {e}')


class AfterLoginScreen(QWidget):
    close_all_windows_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.tecnico_window = None

    def initUI(self):
        self.setWindowTitle('Tela Principal')
        self.setGeometry(100, 100, 800, 600)

        self.all_buttons = {
            'Registrar Produto': QPushButton('Registrar Produto'),
            'Registrar Fornecedor': QPushButton('Registrar Fornecedor'),
            'Registrar Técnico': QPushButton('Registrar Técnico'),
            'Retirar Material': QPushButton('Retirar Material'),
            'Retorno de Material': QPushButton('Retorno de Material'),
            'Mostrar Produtos': QPushButton('Mostrar Produtos'),
            'Mostrar Técnicos': QPushButton('Mostrar Técnicos'),
            'Mostrar Produtos Retirados': QPushButton('Mostrar Produtos Retirados'),
            'Mostrar Estoque Total': QPushButton('Mostrar Estoque Total'),
            'Adicionar Novo Usuário': QPushButton('Adicionar Novo Usuário'),
            'Gerar PDF': QPushButton('Gerar PDF'),
            'Procurar PDF': QPushButton('Procurar PDF')
        }

        self.btn_procurar_pdf = self.all_buttons['Procurar PDF']
        self.btn_gerar_pdf = self.all_buttons['Gerar PDF']
        self.btn_mostrar_tecnicos = self.all_buttons['Mostrar Técnicos']  # Novo botão
        self.btn_procurar_pdf.clicked.connect(self.procurar_pdf)
        self.btn_gerar_pdf.clicked.connect(self.gerar_pdf)
        # self.btn_mostrar_tecnicos.clicked.connect(self.show_tecnicos)  # Conecta o botão ao método

        self.btn_logout = QPushButton()
        self.btn_logout.setObjectName('logoutButton')
        self.btn_logout.setStyleSheet("""
            QPushButton#logoutButton {
                border: none;
                background: none;
                width: 50px;
                height: 50px;
                border-radius: 25px;
                background-color: #0078D4; /* Cor de fundo azul claro */
            }
        """)
        self.set_logout_button_icon('C:/Users/Detel/Desktop/pngwing.com.png', 50, 50)

        # Criação do QTabWidget
        self.tabs = QTabWidget()

        # Aba para registro
        self.tab_register = QWidget()
        self.tab_register_layout = QVBoxLayout()
        self.add_buttons_to_tab(self.tab_register_layout,
                                ['Registrar Produto', 'Registrar Fornecedor', 'Registrar Técnico'])
        self.tab_register.setLayout(self.tab_register_layout)

        # Aba para gestão de materiais
        self.tab_materials = QWidget()
        self.tab_materials_layout = QVBoxLayout()
        self.add_buttons_to_tab(self.tab_materials_layout,
                                ['Retirar Material', 'Retorno de Material', 'Mostrar Produtos',
                                 'Mostrar Produtos Retirados', 'Mostrar Estoque Total'])
        self.tab_materials.setLayout(self.tab_materials_layout)

        # Aba para usuário
        self.tab_user = QWidget()
        self.tab_user_layout = QVBoxLayout()
        self.add_buttons_to_tab(self.tab_user_layout, ['Adicionar Novo Usuário'])
        self.tab_user.setLayout(self.tab_user_layout)

        # Aba para PDFs
        self.tab_pdfs = QWidget()
        self.tab_pdfs_layout = QVBoxLayout()
        self.add_buttons_to_tab(self.tab_pdfs_layout, ['Gerar PDF', 'Procurar PDF', 'Mostrar Técnicos'])
        self.tab_pdfs.setLayout(self.tab_pdfs_layout)

        # Adiciona as abas ao QTabWidget
        self.tabs.addTab(self.tab_register, 'Registro')
        self.tabs.addTab(self.tab_materials, 'Materiais')
        self.tabs.addTab(self.tab_user, 'Usuário')
        self.tabs.addTab(self.tab_pdfs, 'PDFs')

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)

        # Adiciona o botão de logout ao layout principal
        logout_layout = QHBoxLayout()
        logout_layout.addStretch()
        logout_layout.addWidget(self.btn_logout)
        main_layout.addLayout(logout_layout)

        self.setLayout(main_layout)
        self.showMaximized()  # Abre a janela maximizada

    def set_logout_button_icon(self, image_path, width, height):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        icon = QIcon(pixmap)
        self.btn_logout.setIcon(icon)
        self.btn_logout.setIconSize(pixmap.size())

    def closeEvent(self, event):
        self.close_all_windows_signal.emit()
        super().closeEvent(event)

    def habilitar_botao_adicionar_usuario(self):
        self.all_buttons['Adicionar Novo Usuário'].setEnabled(True)

    def desabilitar_botao_adicionar_usuario(self):
        self.all_buttons['Adicionar Novo Usuário'].setEnabled(False)

    def gerar_pdf(self):
        ordem_servico, ok = QInputDialog.getText(self, 'Ordem de Serviço', 'Digite a ordem de serviço:')
        if ok and ordem_servico:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Salvar PDF", f"{ordem_servico}.pdf",
                                                       "PDF Files (*.pdf);;All Files (*)",
                                                       options=options)

            if file_name:
                try:
                    session = Session()
                    retirada = session.query(RetiradaMaterial).filter_by(ordem_servico=ordem_servico).first()

                    if retirada:
                        material_info = {
                            'data_retirada': retirada.data.strftime('%d/%m/%Y'),
                            'nome_tecnico': retirada.tecnico.nome,
                            'matricula_tecnico': retirada.tecnico.matricula,
                            'local_destino': retirada.local,
                            'numero_patrimonio': retirada.patrimonio
                        }

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
        ordem_servico, ok = QInputDialog.getText(self, 'Ordem de Serviço', 'Digite a ordem de serviço:')
        if ok and ordem_servico:
            self.pdf_path = f"{ordem_servico}.pdf"
            if os.path.exists(self.pdf_path):
                self.pdf_viewer = PDFViewer(self.pdf_path)
                self.pdf_viewer.show()
            else:
                QMessageBox.warning(self, 'Arquivo Não Encontrado',
                                    'Nenhum arquivo PDF encontrado para a ordem de serviço fornecida.')

    def add_buttons_to_tab(self, layout, button_names):
        layout.setSpacing(5)  # Ajuste o espaçamento entre os widgets
        layout.setContentsMargins(10, 10, 10, 10)  # Adicione margens internas ao layout

        for name in button_names:
            button = self.all_buttons[name]
            button.setFixedWidth(250)
            button.setFixedHeight(50)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #00B2FF; /* Azul claro */
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #0094D6;
                }
                QPushButton:pressed {
                    background-color: #0072B3;
                }
            """)
            # Cria um layout horizontal para cada botão
            button_layout = QHBoxLayout()
            button_layout.addWidget(button)
            button_layout.setContentsMargins(0, 0, 0, 0)  # Remove as margens internas do layout
            button_layout.setSpacing(5)  # Ajuste o espaçamento entre os widgets

            layout.addLayout(button_layout)


# Exemplo de execução
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = AfterLoginScreen()
    window.show()
    sys.exit(app.exec_())
