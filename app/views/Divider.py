from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class Divider(QWidget):
    def __init__(self, vertical: bool = False, opacity: float = 1):
        super().__init__()
        self.vertical = vertical
        self.opacity = opacity

        if self.vertical:
            # For vertical divider, fix the width to 1px and let the height expand.
            self.setFixedWidth(1)
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        else:
            # For horizontal divider, fix the height to 1px and let the width expand.
            self.setFixedHeight(1)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.gray)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setOpacity(self.opacity)

        if self.vertical:
            # Draw a vertical line centered in the widget.
            x = self.width() // 2
            painter.drawLine(x, 0, x, self.height())
        else:
            # Draw a horizontal line centered in the widget.
            y = self.height() // 2
            painter.drawLine(0, y, self.width(), y)
