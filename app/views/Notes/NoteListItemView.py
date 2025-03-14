from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFontMetrics, QResizeEvent
from PyQt5.QtCore import Qt

from app.controllers.NavigationController import NavigationController
from app.enums.route import Route
from app.utils import style_h2


class NoteListItemView(QWidget):
    def __init__(self, note: dict, nav_controller: NavigationController):
        super().__init__()
        self.nav_controller = nav_controller
        self.full_text = note['text']

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.setObjectName("NoteListItemView")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet("""
            #NoteListItemView {
                background-color: rgba(255,215,100, 0.5);
                border-radius: 8px;
            }
        """)

        self.title_label = QLabel(note['title'])
        style_h2(self.title_label)

        self.text_label = QLabel()
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignTop)

        self.details_btn = QPushButton("Details")
        self.details_btn.clicked.connect(lambda: self.nav_controller.navigate(Route.NOTE_DETAIL, note=note))
        self.details_btn.setMaximumWidth(80)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.text_label)
        self.layout.addStretch()
        self.layout.addWidget(self.details_btn)

        self.setLayout(self.layout)

        self.truncate_text()

    def truncate_text(self):
        """Truncate the text to fit within 3 lines and append '...' if necessary."""
        if not self.full_text:
            self.text_label.setText("")
            return

        font_metrics = QFontMetrics(self.text_label.font())
        line_height = font_metrics.lineSpacing()
        max_height = 3 * line_height

        available_width = self.text_label.width() - 10
        if available_width <= 0:
            available_width = 200

        rect = font_metrics.boundingRect(0, 0, available_width, 10000, Qt.TextWordWrap, self.full_text)
        if rect.height() <= max_height:
            self.text_label.setText(self.full_text)
            return

        truncated_text = ""
        for i in range(1, len(self.full_text) + 1):
            test_text = self.full_text[:i] + "..."
            rect = font_metrics.boundingRect(0, 0, available_width, 10000, Qt.TextWordWrap, test_text)
            if rect.height() > max_height:
                break
            truncated_text = test_text

        self.text_label.setText(truncated_text)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.truncate_text()
