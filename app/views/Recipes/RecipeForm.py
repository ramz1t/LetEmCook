from typing import Callable

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy
from app.views.FormInput import FormInput
from app.views.Recipes.IngredientsPicker import IngredientsPicker


class RecipeForm(QWidget):
    """A form widget for creating or editing a recipe with name, description, and ingredients.

    This widget provides input fields for a recipe's name and description, an ingredients picker,
    and a submit button. It collects the data and passes it to a callback function when submitted.

    Attributes:
        submit_callback: Function to call with the recipe data upon submission.
        initial_recipe: Optional dictionary containing initial recipe data (name, description, ingredients).
                Defaults to None.
    """

    def __init__(self, submit_callback: Callable[[dict], None], initial_recipe: dict = None):
        super().__init__()
        self.submit_callback = submit_callback
        self.initial_recipe = initial_recipe
        self.ingredients = []
        if initial_recipe:
            self.ingredients = [(ing['id'], ing['quantity']) for ing in initial_recipe['ingredients']]

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
            margins=[0, 10, 0, 0]
        )
        self.layout.addWidget(self.description_input)

        ingredients_picker = IngredientsPicker(
            ingredients=initial_recipe["ingredients"] if initial_recipe is not None else [],
            set_ingredients=self.__set_ingredients
        )
        self.layout.addWidget(ingredients_picker)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_data)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def submit_data(self):
        """Collect form data and pass it to the submit callback.

        Gathers the current values from the name input, description input, and ingredients list,
        constructs a dictionary, and invokes the submit_callback with the data.
        """
        name = self.name_input.text.strip()
        description = self.description_input.text.strip()

        if not name or not description:
            return

        data = {
            "name": name,
            "description": description,
            "ingredients": self.ingredients
        }

        self.submit_callback(data)

    def __set_ingredients(self, ingredients: list[tuple[int, float]]):
        """Update the ingredients list with new values from the IngredientsPicker.

        Args:
            ingredients: List of tuples (ingredient_id, quantity) representing selected ingredients.
        """
        self.ingredients = ingredients