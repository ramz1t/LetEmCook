from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox

class CustomDialog(QDialog):
    """
    A custom dialog that displays a title, a message, and a customizable confirm button.

    Parameters:
        title: The title of the dialog.
        message: The message content displayed in the dialog.
        confirm_text: The text displayed on the confirm button. Default is "Confirm".
        parent: The parent widget, if any.
    """
    def __init__(
        self,
        title: str,
        message: str,
        confirm_text: str = "Confirm",
        parent=None,
    ):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
            font-weight: bold;
            font-size: 14px;
        """)
        self.title_label.setWordWrap(True)
        self.layout.addWidget(self.title_label)

        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.layout.addWidget(self.message_label)

        # Create a button box
        self.button_box = QDialogButtonBox()

        # Add primary Cancel button
        self.cancel_button = self.button_box.addButton(QDialogButtonBox.Cancel)
        self.cancel_button.setDefault(True)

        # Add the custom confirm button with the provided text.
        self.confirm_button = self.button_box.addButton(confirm_text, QDialogButtonBox.AcceptRole)

        # Connect signals for accept and reject actions.
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)
