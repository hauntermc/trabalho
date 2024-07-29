from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class OrderOfServiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Entrada da Ordem de Serviço')
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f4f8;  /* Azul claro */
                font-family: Arial, sans-serif;
            }
            QLineEdit {
                border: 1px solid #007acc;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                background-color: #ffffff;
                min-width: 200px;  # Define a largura mínima
                max-width: 200px;  # Define a largura máxima
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)

        layout = QVBoxLayout()

        self.order_of_service_line_edit = QLineEdit()
        self.order_of_service_line_edit.setPlaceholderText("Digite a Ordem de Serviço")
        layout.addWidget(self.order_of_service_line_edit)

        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def get_order_of_service(self):
        return self.order_of_service_line_edit.text()
