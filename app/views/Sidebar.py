from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout

from config import NAVIGATION


class Sidebar(QWidget):
    def __init__(self, nav_controller):
        super().__init__()

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        nav_title = QLabel("Let'EmCook")
        nav_title.setStyleSheet("""
            font-weight: bold; 
            font-size: 18px; 
            border-bottom: 1px solid gray; 
            padding: 10px; 
            background: transparent;
        """)
        sidebar_layout.addWidget(nav_title)

        for index, option in enumerate(NAVIGATION):
            sidebar_layout.addWidget(
                SidebarButton(
                    icon=option["icon"],
                    title=option["title"],
                    navigate=partial(nav_controller.navigate, option["route"])
                )
            )

        sidebar_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(sidebar_layout)
        self.setStyleSheet("border-right: 1px solid gray; background: transparent;")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)


class SidebarButton(QPushButton):
    def __init__(self, icon, title, navigate):
        super().__init__(icon + "  " + title)

        self.clicked.connect(navigate)
        self.setStyleSheet("""
            text-align: left;
            border: 0px solid transparent;
            padding: 10px 15px;
            font-weight: bold;
        """)
        self.setCursor(Qt.PointingHandCursor)
