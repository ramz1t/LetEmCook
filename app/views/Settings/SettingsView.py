from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.controllers.NavigationController import NavigationController
from app.views.Settings.BodyMetricsView import BodyMetricsForm
from app.views.Divider import Divider
from app.views.TopBar import TopBar


class SettingsView(QWidget):
    def __init__(self, nav_controller: NavigationController):
        super().__init__()

        self.nav_controller = nav_controller

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layout.addWidget(
            TopBar(
                title="Settings",
                nav_controller=nav_controller,
                is_root_view=True,
            )
        )
        self.layout.addWidget(Divider())

        self.layout.addWidget(BodyMetricsForm())

        self.setLayout(self.layout)