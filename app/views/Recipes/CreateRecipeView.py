from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from app.controllers.NavigationController import NavigationController
from app.controllers.RecipesController import RecipesController
from app.views.Divider import Divider
from app.views.TopBar import TopBar


class CreateRecipeView(QWidget):
    def __init__(self, nav_controller: NavigationController):
        super().__init__()
        self.nav_controller = nav_controller
        self.recipes_controller = RecipesController()
        self.ingredients = []
        self.name = ""
        self.description = ""

        # Create recipe button
        self.create_btn = QPushButton("Create")
        self.create_btn.clicked.connect(lambda: self.__create_recipe())

        # Page layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Set page TopBar
        layout.addWidget(
            TopBar(
                title="Create New Recipe",
                nav_controller=self.nav_controller,
                actions=[self.create_btn],
            )
        )
        layout.addWidget(Divider())

        self.setLayout(layout)

    def __create_recipe(self):
        recipe = self.recipes_controller.create(
            ingredients=self.ingredients,
            name=self.name,
            description=self.description
        )
        if recipe:
            self.nav_controller.pop_route()