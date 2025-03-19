from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from app.controllers.NavigationController import NavigationController
from app.controllers.RecipesController import RecipesController
from app.enums.route import Route
from app.views.Divider import Divider
from app.views.Recipes.RecipeForm import RecipeForm
from app.views.TopBar import TopBar


class CreateRecipeView(QWidget):
    def __init__(self, nav_controller: NavigationController):
        super().__init__()
        self.nav_controller = nav_controller
        self.recipes_controller = RecipesController()
        self.ingredients = []
        self.name = ""
        self.description = ""

        # Page layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.form = RecipeForm(self.__create_recipe)

        self.create_btn = QPushButton("Create")
        self.create_btn.clicked.connect(lambda: self.form.submit_data())

        # Set page TopBar
        layout.addWidget(
            TopBar(
                title="Create New Recipe",
                nav_controller=self.nav_controller,
                actions=[self.create_btn]
            )
        )
        layout.addWidget(Divider())

        layout.addWidget(self.form)

        self.setLayout(layout)

    def __create_recipe(self, data: dict):
        recipe = self.recipes_controller.create(**data)
        if recipe:
            self.nav_controller.navigate(Route.RECIPE_DETAIL, recipe=recipe)