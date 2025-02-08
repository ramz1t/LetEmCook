from PyQt5.QtWidgets import QLabel, QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.label = QLabel('Welcome to LetEmCook!', self)
        self.setWindowTitle('LetEmCook App')
        self.setGeometry(100, 100, 300, 200)
