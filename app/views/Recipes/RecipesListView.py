from typing import Optional

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from app.controllers.NavigationController import NavigationController
from app.controllers.RecipesController import RecipesController
from app.enums.route import Route
from app.views.Divider import Divider
from app.views.Recipes.RecipesListItemView import RecipesListItemView
from app.views.SearchBar import SearchBar
from app.views.TopBar import TopBar


class RecipesListView(QWidget):
    """
        A view that displays a list of recipes with a search bar and navigation controls.

        Args:
            nav_controller: Controller to manage navigation between views.
            q: An optional search query to filter the displayed recipes. Defaults to an empty string.
    """
    def __init__(self, nav_controller: NavigationController, q: Optional[str] = str()):
        super().__init__()
        self.nav_controller = nav_controller
        self.recipes_controller = RecipesController()

        # Create recipe button
        self.create_recipe_btn = QPushButton("Create New Recipe")
        self.create_recipe_btn.clicked.connect(lambda: self.nav_controller.navigate(Route.RECIPE_CREATE))

        # Page layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Set page TopBar
        self.layout.addWidget(
            TopBar(
                title='Recipes',
                nav_controller=nav_controller,
                actions=[
                    self.create_recipe_btn,
                    SearchBar(
                        on_search=self.__search,
                        placeholder="Search Recipes...",
                    ),
                ],
                is_root_view=not q, # If search is active, user can click "<-" button to go back to all recipes
            )
        )
        self.layout.addWidget(Divider())

        # Create recipes list
        self.recipes = self.recipes_controller.list_recipes(search=q)
        if self.recipes:
            for idx, recipe in enumerate(self.recipes):
                self.layout.addWidget(
                    RecipesListItemView(
                        recipe=recipe,
                        nav_controller=self.nav_controller,
                    )
                )
                self.layout.addWidget(Divider(opacity=0.3))
        else:
            self.layout.addWidget(QLabel("No recipes found")) # TODO: replace with NoContentView

        self.setLayout(self.layout)

    def __search(self, search: str) -> None:
        self.nav_controller.navigate(Route.RECIPES, q=search)
