from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from app.controllers.NavigationController import NavigationController
from app.enums.route import Route
from app.views.Divider import Divider
from app.views.InfoContainer import InfoContainer
from app.views.TopBar import TopBar


class NoteDetailView(QWidget):
    def __init__(self, note: dict, nav_controller: NavigationController):
        super().__init__()
        self.note = note
        self.nav_controller = nav_controller

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(lambda: self.nav_controller.navigate(Route.NOTE_EDIT, note=note))

        self.layout.addWidget(
            TopBar(
                title=note['title'],
                nav_controller=nav_controller,
                actions=[self.edit_btn]
            )
        )
        self.layout.addWidget(Divider())

        self.text_label = QLabel(note['text'])
        self.text_label.setWordWrap(True)
        self.text_label.setStyleSheet("""font-size: 18px; padding: 15px;""")

        self.layout.addWidget(InfoContainer(self.text_label, '15px'))

        self.setLayout(self.layout)