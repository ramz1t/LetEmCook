from typing import Callable

from PyQt5.QtCore import Qt


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit

class SearchBar(QWidget):
    """
    A search bar widget with a text field and a search button.

    Attributes:
        on_search: A callback function to handle search queries.
        placeholder: Placeholder text for text field.
        show_dismiss: Flag to show dismiss button.
        initial_value: Initial value for the search bar.
    """
    def __init__(
            self,
            on_search: Callable[[str], None],
            placeholder: str = str(),
            show_dismiss: bool = False,
            initial_value: str = None,
    ):
        super().__init__()
        self.on_search = on_search
        self.q = ""
        self.placeholder = placeholder
        self.initial_value = initial_value

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignVCenter)

        # Text field for search input
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText(placeholder)
        self.search_field.textChanged.connect(self.__update_query)

        if initial_value:
            self.search_field.setText(initial_value)

        # Search button
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(lambda: self.on_search(self.q))

        layout.addWidget(self.search_field)
        layout.addWidget(self.search_btn)

        if show_dismiss:
            # Dismiss button
            self.dismiss_btn = QPushButton("Dismiss")
            self.dismiss_btn.clicked.connect(lambda: self.on_search(""))
            layout.addWidget(self.dismiss_btn)

        self.setLayout(layout)

    def __update_query(self, text: str):
        """
        Update the search query based on the text entered in the text field.
        :param text: The current text in the search field.
        """
        self.q = text



