from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QStackedLayout, QLabel, \
    QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QIcon

from app.views.Sidebar import Sidebar
from config import NAVIGATION

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LetEmCook")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar
        self.sidebar = Sidebar(navigate=self.show_page)
        main_layout.addWidget(self.sidebar)

        # Create content area
        self.content_area = QVBoxLayout()

        # Create page title
        self.page_title = QLabel("")
        self.content_area.addWidget(self.page_title)

        # Create page container
        self.page_container = QStackedLayout()
        self.content_area.addLayout(self.page_container)

        self.content_area.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set main widget and content area
        main_layout.addLayout(self.content_area)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_page(self, index):
        current_page = self.page_container.currentWidget()

        if current_page:
            self.page_container.removeWidget(current_page)
            current_page.deleteLater()

        new_page = NAVIGATION[index]["view_factory"]()
        self.page_container.addWidget(new_page)
        self.page_container.setCurrentWidget(new_page)

        self.page_title.setText(NAVIGATION[index]["title"])
        self.page_title.setStyleSheet(
            "font-weight: bold; font-size: 18px; border-bottom: 1px solid gray; padding: 10px; background: transparent;"
        )
