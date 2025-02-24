# --- For frontend ---
from PyQt5.QtWidgets import QLayout, QLabel


def get_recipes_count_label(count: int) -> str:
    if count > 1:
        return f"{count} ingredients"
    elif count == 1:
        return f"1 ingredient"
    else:
        return "No ingredients"

def clear_layout(layout: QLayout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()

def style_h1(label: QLabel):
    label.setStyleSheet("""
        font-weight: bold;
        font-size: 18px;
    """)

def style_h2(label: QLabel):
    label.setStyleSheet("""
        font-weight: bold;
        font-size: 14px;
    """)

        # --- For backend ---