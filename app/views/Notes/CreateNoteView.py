from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from app.controllers.NavigationController import NavigationController
from app.controllers.NotesController import NotesController
from app.enums.route import Route
from app.views.Divider import Divider
from app.views.Notes.NoteForm import NoteForm
from app.views.TopBar import TopBar


class CreateNoteView(QWidget):
    def __init__(self, nav_controller: NavigationController):
        super().__init__()
        self.nav_controller = nav_controller
        self.notes_controller = NotesController()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.form = NoteForm(self.__create_note)
        self.create_btn = QPushButton("Create")
        self.create_btn.clicked.connect(lambda: self.form.submit_data())

        self.layout.addWidget(
            TopBar(
                title="Create Note",
                nav_controller=self.nav_controller,
                actions=[self.create_btn]
            )
        )
        self.layout.addWidget(Divider())
        self.layout.addWidget(self.form)

        self.setLayout(self.layout)

    def __create_note(self, data: dict):
        created_note = self.notes_controller.create(**data)
        if created_note:
            self.nav_controller.navigate(Route.NOTE_DETAIL, note=created_note)