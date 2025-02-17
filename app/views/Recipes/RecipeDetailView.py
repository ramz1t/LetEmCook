from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout

from app.controllers.NavigationController import NavigationController
from app.enums.route import Route
from app.views.Divider import Divider
from app.views.InfoContainer import InfoContainer
from app.views.Recipes.IngredientsList import IngredientsList
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

        # Description label
        self.description_label = QLabel(recipe["description"])
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("padding: 10px;")
        self.layout.addWidget(InfoContainer(self.description_label, margin="20px"))

        # Place where ingredients list will be added
        self.ingredients_container = QWidget()
        self.ingredients_container_layout = QVBoxLayout()
        self.ingredients_container_layout.setContentsMargins(0, 0, 0, 0)
        self.ingredients_container_layout.setSpacing(0)
        self.ingredients_container.setLayout(self.ingredients_container_layout)

        self.layout.addWidget(IngredientsList(recipe["ingredients"], self.__set_sorting))

        self.setLayout(self.layout)

    def __set_sorting(self, key: str) -> None:
        print("sorting set to", key)
        pass
