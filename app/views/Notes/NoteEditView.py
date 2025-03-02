from PyQt5.QtWidgets import QWidget, QFormLayout, QVBoxLayout, QPushButton, QDialog

from app.controllers.NavigationController import NavigationController
from app.controllers.NotesController import NotesController
from app.enums.route import Route
from app.views.CustomDialog import CustomDialog
from app.views.Divider import Divider
from app.views.Notes.NoteForm import NoteForm
from app.views.TopBar import TopBar


class NoteEditView(QWidget):
    def __init__(self, note: dict, nav_controller: NavigationController):
        super().__init__()
        self.note = note
        self.nav_controller = nav_controller
        self.notes_controller = NotesController()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setStyleSheet("color: red;")
        self.delete_btn.clicked.connect(lambda: self.__show_confirmation_dialog())

        self.layout.addWidget(
            TopBar(
                title="Edit Note",
                nav_controller=self.nav_controller,
                actions=[self.delete_btn]
            )
        )
        self.layout.addWidget(Divider())

        self.layout.addWidget(NoteForm(self.__update_note, initial_note=note))

        self.setLayout(self.layout)

    def __show_confirmation_dialog(self):
        dialog = CustomDialog(
            "Would you like to delete this note?",
            "This note will be deleted from the list. This action cannot be undone.",
            "Delete"
        )

        if dialog.exec_() == QDialog.Accepted:
            self.__delete_note()

    def __delete_note(self):
        deleted = self.notes_controller.delete(id=self.note['id'])
        if deleted:
            self.nav_controller.navigate(Route.NOTES)

    def __update_note(self, data: dict):
        updated_note = self.notes_controller.update(id=self.note['id'], **data)
        if updated_note:
            self.nav_controller.navigate(Route.NOTES)
            self.nav_controller.navigate(Route.NOTE_DETAIL, note=updated_note)
