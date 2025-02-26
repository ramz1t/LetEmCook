from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFrame

from app.controllers.NavigationController import NavigationController


class TopBar(QFrame):
    """
    A custom top bar widget for displaying a title, optional actions, and navigation controls.

    Attributes:
        title: The title displayed in the center of the top bar.
        nav_controller: The navigation controller used to handle navigation events.
        actions: A list of widgets (e.g., buttons) displayed as actions on the right side of the top bar.
        is_root_view: A flag indicating whether the current view is the root view.
                             If True, the back button will not be displayed.
    """
    def __init__(
        self,
        title: str,
        nav_controller: NavigationController,
        actions: Optional[list[QWidget]] = None,
        is_root_view: bool = False,
    ):
        super().__init__()

        self.title = title
        self.nav_controller = nav_controller
        self.actions = actions if actions is not None else []
        self.is_root_view = is_root_view

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignVCenter)
        self.layout.setContentsMargins(20, 7, 20, 0)
        self.layout.setSpacing(20)
        self.setFixedHeight(60)

        # Back button
        if not self.is_root_view:
            back_button = QPushButton("←")
            back_button.clicked.connect(lambda: self.nav_controller.pop_route())
            self.layout.addWidget(back_button)

        # Title
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-weight: bold;
            font-size: 18px;
            margin-right: auto;
        """)
        self.layout.addWidget(title_label)

        self.layout.addStretch(1)

        # Actions
        if self.actions:
            actions_layout = QHBoxLayout()
            actions_layout.setAlignment(Qt.AlignVCenter)
            for action in self.actions:
                self.layout.addWidget(action)
            self.layout.addLayout(actions_layout)

        self.setLayout(self.layout)
