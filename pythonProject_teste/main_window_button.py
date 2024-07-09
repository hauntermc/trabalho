from PyQt5.QtWidgets import QAction, QMessageBox

class MainWindowButtons:
    def __init__(self, main_window):
        self.main_window = main_window

    def get_register_tecnico_action(self):
        action = QAction('Registrar Técnico', self.main_window)
        action.triggered.connect(self.main_window.open_register_tecnico_window)
        return action


    def get_register_product_action(self):
        action = QAction('Registrar Produto', self.main_window)
        action.triggered.connect(self.main_window.open_register_product_window)
        return action

    def get_logout_action(self):
        action = QAction('Logout', self.main_window)
        action.triggered.connect(self.main_window.logout)
        return action
