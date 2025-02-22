from typing import Callable

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy
from app.views.FormInput import FormInput
from app.views.Recipes.IngredientsPicker import IngredientsPicker


class RecipeForm(QWidget):
    def __init__(self, submit_callback: Callable[[dict], None], initial_recipe: dict = None):
        super().__init__()
        self.submit_callback = submit_callback
        self.ingredients: list[tuple[int, float]] = []
        if initial_recipe:
            self.ingredients = [(ing['id'], ing['quantity']) for ing in initial_recipe['ingredients']]

        # Ensure the widget expands to take the full available width.
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(60, 15, 60, 15)

        self.name_input = FormInput(
            title="Name:",
            initial_text=initial_recipe['name'] if initial_recipe else "",
        )
        self.layout.addWidget(self.name_input)

        self.description_input = FormInput(
            title="Description:",
            initial_text=initial_recipe['description'] if initial_recipe else "",
            is_multiline=True,
            margins=[0,10,0,0]
        )
        self.layout.addWidget(self.description_input)

        ingredients_picker = IngredientsPicker(
            ingredients=initial_recipe["ingredients"] if initial_recipe is not None else [],
            set_ingredients=self.__set_ingredients
        )
        self.layout.addWidget(ingredients_picker)

        # Submit button.
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_data)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def submit_data(self):
        name = self.name_input.text
        description = self.description_input.text

        data = {
            "name": name,
            "description": description,
            "ingredients": self.ingredients
        }

        self.submit_callback(data)

    def __set_ingredients(self, ingredients: list[tuple[int, float]]):
        self.ingredients = ingredients
