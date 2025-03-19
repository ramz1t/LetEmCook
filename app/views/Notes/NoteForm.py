from typing import Callable

from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.views.FormInput import FormInput


class NoteForm(QWidget):
    def __init__(self, submit_callback: Callable[[dict], None], initial_note: dict = None):
        super().__init__()
        self.initial_note = initial_note
        self.submit_callback = submit_callback

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(60, 15, 60, 15)

        self.title_input = FormInput(
            title="Title",
            initial_text=initial_note["title"] if initial_note else ""
        )
        self.text_input = FormInput(
            title="Text",
            initial_text=initial_note["text"] if initial_note else "",
            is_multiline=True
        )

        self.layout.addWidget(self.title_input)
        self.layout.addWidget(self.text_input)

        self.setLayout(self.layout)

    def submit_data(self):
        title = self.title_input.text.strip()
        text = self.text_input.text.strip()

        if not title or not text:
            return

        data = {
            "title": title,
            "text": text,
        }

        self.submit_callback(data)
