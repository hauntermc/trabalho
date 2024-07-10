from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QRectF, Qt


class PrintHandler:
    def __init__(self, parent):
        self.parent = parent

    def print_report(self):
        try:
            printer = QPrinter(QPrinter.HighResolution)
            print_dialog = QPrintDialog(printer, self.parent)

            if print_dialog.exec_() == QPrintDialog.Accepted:
                pixmap = QPixmap(self.parent.size())
                pixmap.fill(Qt.white)  # Preenche o pixmap com fundo branco para garantir que não esteja vazio

                painter = QPainter(pixmap)
                self.parent.render(painter)
                painter.end()

                painter = QPainter(printer)
                target_rect = printer.pageRect(QPrinter.DevicePixel)
                source_rect = QRectF(pixmap.rect())
                painter.drawPixmap(target_rect, pixmap, source_rect)
                painter.end()

                # Após imprimir, perguntar se deseja salvar a imagem
                reply = QMessageBox.question(self.parent, 'Salvar Imagem', 'Deseja salvar a imagem impressa?',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    file_path, _ = QFileDialog.getSaveFileName(self.parent, "Salvar Imagem", "",
                                                               "Images (*.png *.jpg *.bmp)")
                    if file_path:
                        if pixmap.save(file_path):
                            QMessageBox.information(self.parent, "Imagem Salva", f"Imagem salva em {file_path}")
                        else:
                            QMessageBox.warning(self.parent, "Erro ao Salvar", "Não foi possível salvar a imagem.")

        except Exception as e:
            QMessageBox.critical(self.parent, "Erro", f"Ocorreu um erro ao imprimir: {str(e)}")
