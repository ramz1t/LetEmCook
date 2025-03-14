from typing import Optional

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QGridLayout, QHBoxLayout, QSizePolicy

from app.controllers.NavigationController import NavigationController
from app.controllers.NotesController import NotesController
from app.controllers.StorageManager import StorageManager
from app.enums.route import Route
from app.enums.storage import StorageKey
from app.views.Divider import Divider
from app.views.NoContentView import NoContentView
from app.views.Notes.NoteListItemView import NoteListItemView
from app.views.SearchBar import SearchBar
from app.views.TopBar import TopBar


class NotesListView(QWidget):
    def __init__(self, nav_controller: NavigationController, q: Optional[str] = str()):
        super().__init__()
        self.nav_controller = nav_controller
        self.notes_controller = NotesController()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.create_note_btn = QPushButton("Create New Note")
        self.create_note_btn.clicked.connect(lambda: self.nav_controller.navigate(Route.NOTE_CREATE))

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(2)
        self.slider.setMaximum(4)
        self.slider.setValue(StorageManager.get_value(StorageKey.NotesGridStep.value, 2))
        self.slider.valueChanged.connect(self.__update_columns)

        layout.addWidget(
            TopBar(
                title="Notes",
                nav_controller=self.nav_controller,
                is_root_view=not q,
                actions=[
                    self.create_note_btn,
                    SearchBar(
                        on_search=self.__search,
                        placeholder="Search Notes...",
                        initial_value=q
                    ),
                    self.slider,
                ]
            )
        )
        layout.addWidget(Divider())

        notes = self.notes_controller.list(search=q)

        if notes:
            # Create container widgets for each note
            self.note_cells = []
            for note in notes:
                cell = QWidget()
                cell.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

                cell_layout = QHBoxLayout()
                cell_layout.setContentsMargins(0, 0, 0, 0)

                note_widget = NoteListItemView(note=note, nav_controller=self.nav_controller)
                note_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

                cell_layout.addWidget(note_widget, stretch=1)

                cell.setLayout(cell_layout)
                self.note_cells.append(cell)

            # Set up the grid layout
            self.grid_layout = QGridLayout()
            self.grid_layout.setContentsMargins(15, 15, 15, 15)
            self.grid_layout.setHorizontalSpacing(15)
            self.grid_layout.setVerticalSpacing(15)
            layout.addLayout(self.grid_layout)

            for index, cell in enumerate(self.note_cells):
                row = index // self.slider.value()
                col = index % self.slider.value()
                self.grid_layout.addWidget(cell, row, col)

            for col in range(self.slider.value()):
                self.grid_layout.setColumnStretch(col, 1)
        else:
            layout.addWidget(
                NoContentView(
                    title=f'No Results for "{q}"',
                    description="No notes found. Check the spelling or try a new search.",
                    margins=[0, 160, 0, 0]
                )
            )

        self.setLayout(layout)

    def __search(self, search: str) -> None:
        self.nav_controller.navigate(Route.NOTES, q=search)

    def __update_columns(self, value: int):
        """Update the grid layout when the slider value changes."""
        StorageManager.set_value(StorageKey.NotesGridStep.value, value)
        QTimer.singleShot(0, self.nav_controller.reload)