from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy

from config import NAVIGATION


class Sidebar(QWidget):
    def __init__(self, navigate):
        super().__init__()

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        nav_title = QLabel("Let'EmCook")
        nav_title.setStyleSheet(
            "font-weight: bold; font-size: 18px; border-bottom: 1px solid gray; padding: 10px; background: transparent;")
        sidebar_layout.addWidget(nav_title)

        for index, option in enumerate(NAVIGATION):
            btn = QPushButton(option["title"])
            btn.setIcon(QIcon(option["icon"]))
            btn.clicked.connect(lambda _, idx=index: navigate(idx))
            btn.setStyleSheet("border: 0px solid transparent; padding: 10px 5px;")
            btn.setCursor(Qt.PointingHandCursor)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(sidebar_layout)
        self.setStyleSheet("border-right: 1px solid gray;")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)