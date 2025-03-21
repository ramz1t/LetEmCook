from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QTextEdit, QLineEdit, QSizePolicy, QMessageBox, QPushButton, \
    QVBoxLayout

from app.ai import generate_enhanced_text
from app.utils import style_h2


class FormInput(QWidget):
    """A customizable input widget with a label, supporting single-line or multi-line text entry.

    This widget combines a label with either a `QLineEdit` (single-line) or `QTextEdit` (multi-line)
    input field, arranged horizontally. It updates its internal `text` property whenever the user
    modifies the input and supports initial text and custom margins.

    Attributes:
        text: The current text content of the input field.
        initial_text: The initial text provided during instantiation.
        is_multiline: Whether the input is multi-line (`QTextEdit`) or single-line (`QLineEdit`).
        margins: The margins applied to the layout [left, top, right, bottom].
        enhanceable: The field can be enhanced using through LLM request.

    Examples:
        >>> single_line = FormInput("Name", "John Doe")
        >>> multi_line = FormInput("Description", "Enter details here", is_multiline=True, margins=[10, 5, 10, 5])
    """

    def __init__(
            self,
            title: str,
            initial_text: str = "",
            is_multiline: bool = False,
            margins: list[int] | None = None,
            enhanceable: bool = False,
    ):
        super().__init__()
        self.text = initial_text
        self.initial_text = initial_text
        self.is_multiline = is_multiline
        self.margins = margins if margins is not None else [0, 0, 0, 0]
        self.enhanceable = enhanceable

        self.__original_text = self.initial_text

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(*self.margins)
        self.layout.setSpacing(15)

        self.label = QLabel(title)
        style_h2(self.label)
        self.label.setMinimumWidth(120)
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

        if self.enhanceable:
            self.buttons = QVBoxLayout()
            self.enhance_btn = QPushButton("MistralAI")
            self.enhance_btn.setIcon(QIcon('./resources/images/mistral-ai-icon.png'))
            self.enhance_btn.clicked.connect(self.__enhance)
            self.rollback_btn = QPushButton("Rollback")
            self.rollback_btn.clicked.connect(self.__rollback)
            self.buttons.addWidget(self.enhance_btn)
            self.buttons.addWidget(self.rollback_btn)
            self.layout.addLayout(self.buttons)

        self.setLayout(self.layout)

    def __update_text(self):
        """
        Update the internal `text` attribute when the input content changes.
        """
        if self.is_multiline:
            self.text = self.input.toPlainText()
        else:
            self.text = self.input.text()

    def __enhance(self):
        if not self.text:
            QMessageBox.warning(self,
                                "Empty text",
                                "Please enter text to enhance. eg. Russian dumplings recipe, Cheap asian recipe with shrimps etc.")
            return

        self.__original_text = self.text

        try:
            enhanced_text = generate_enhanced_text(self.text)
        except ConnectionError as e:
            QMessageBox.warning(self, "Connection error", str(e))
            return

        self.__set_new_value(enhanced_text)

    def __rollback(self):
        self.__set_new_value(self.__original_text)

    def __set_new_value(self, new_value: str):
        self.text = new_value
        self.input.setText(new_value)