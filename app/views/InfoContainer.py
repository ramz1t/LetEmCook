from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import QEvent


class InfoContainer(QWidget):
    def __init__(self, child_view: QWidget, margin: str = str()):
        super().__init__()
        self.child_view = child_view
        self.margin = margin

        # Store the current background color to avoid unnecessary updates
        self._current_background = None

        self.setObjectName("InfoContainer")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self._update_style()

        self.layout.addWidget(self.child_view)
        self.setLayout(self.layout)

    def _update_style(self):
        """
        Update the background color based on the current palette,
        using the system Window color but slightly brighter.
        """
        # Get the system's window color from the application palette
        palette = QApplication.instance().palette()
        window_color = palette.color(QPalette.Window)

        # Make the window color slightly brighter (e.g., 20% brighter with factor 120)
        new_color_qcolor = window_color.lighter(120)
        new_color = new_color_qcolor.name()  # Convert to a hex string (e.g., "#ffffff")

        if new_color != self._current_background:
            self._current_background = new_color
            self.setStyleSheet(f"""
                background-color: {new_color};
                border-radius: 10px;
                margin: {self.margin};
            """)

    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.PaletteChange:
            self._update_style()
        super().changeEvent(event)
