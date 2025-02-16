from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from app.controllers.NavigationController import NavigationController
from app.enums.route import Route
from app.views.Divider import Divider
from app.views.TopBar import TopBar


class RecipeDetailView(QWidget):
    def __init__(self, recipe: dict, nav_controller: NavigationController):
        super().__init__()
        self.recipe = recipe
        self.nav_controller = nav_controller

        # Page layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Edit button
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(lambda: self.nav_controller.navigate(Route.RECIPE_EDIT, recipe=recipe))

        # Set TopBar
        self.layout.addWidget(
            TopBar(
                title=recipe["name"],
                nav_controller=self.nav_controller,
                actions=[self.edit_btn]
            )
        )
        self.layout.addWidget(Divider())

        self.description_label = QLabel(recipe["description"])
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("""
            background: white;
            margin: 20px;
            padding: 10px;
            border-radius: 10px;
        """)
        self.layout.addWidget(self.description_label)

        self.setLayout(self.layout)