from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from app.controllers.NavigationController import NavigationController
from app.utils import style_h2
from app.views.Settings.BodyMetricsForm import BodyMetricsForm
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

        self.layout.addWidget(BodyMetricsForm(self.nav_controller))

        self.setLayout(self.layout)