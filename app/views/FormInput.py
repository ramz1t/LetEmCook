from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QTextEdit, QLineEdit, QSizePolicy

from app.utils import style_h2


class FormInput(QWidget):
    def __init__(
            self,
            title: str,
            initial_text: str = "",
            is_multiline: bool = False,
            margins: list[int] = None
    ):
        super().__init__()
        self.text = initial_text
        self.initial_text = initial_text
        self.is_multiline = is_multiline
        self.margins = margins if margins is not None else [0, 0, 0, 0]

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(*self.margins)
        self.layout.setSpacing(15)

        self.label = QLabel(title)
        style_h2(self.label)
        self.label.setMinimumWidth(150)
        self.label.setAlignment(Qt.AlignTop)

        if is_multiline:
            self.input = QTextEdit()
        else:
            self.input = QLineEdit()

        self.input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.input.textChanged.connect(self.__update_text)

        if initial_text:
            self.input.setText(initial_text)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)

        self.setLayout(self.layout)

    def __update_text(self):
        if self.is_multiline:
            self.text = self.input.toPlainText()
        else:
            self.text = self.input.text()