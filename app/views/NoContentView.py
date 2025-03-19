from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

class NoContentView(QWidget):
    def __init__(self, title: str, description: str, margins: list[int] = None):
        super().__init__()
        self.title = title
        self.description = description
        self.margins = margins if margins is not None else [0,0,0,0]

        self.layout = QVBoxLayout()

        self.layout.setAlignment(Qt.AlignVCenter)

        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.title_label, alignment=Qt.AlignHCenter)

        self.description_label = QLabel(self.description)
        self.description_label.setStyleSheet("font-size: 18px; font-weight: semibold;")
        self.layout.addWidget(self.description_label, alignment=Qt.AlignHCenter)

        self.setLayout(self.layout)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setContentsMargins(*self.margins)
