from typing import Callable

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy, QLineEdit

from app.controllers.RecipesController import RecipesController
from app.utils import clear_layout, style_h2
from app.views.SearchBar import SearchBar

class IngredientsPicker(QWidget):
    def __init__(self, ingredients: list[dict], set_ingredients: Callable[[list[tuple[int, float]]], None]):
        super().__init__()
        # Initializes selected ingredients as a dict mapping id -> ingredient dict.
        # Each ingredient dict is expected to have 'id', 'name', 'unit' and 'quantity'
        self.selected_ingredients = {ingredient['id']: ingredient for ingredient in ingredients}
        self.set_ingredients = set_ingredients
        self.recipes_controller = RecipesController()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Header for Added Ingredients section
        added_ingredients_header = QWidget()
        added_ingredients_header_layout = QHBoxLayout()
        added_ingredients_header_layout.setContentsMargins(0, 20, 0, 10)
        added_ingredients_title = QLabel("Added Ingredients:")
        style_h2(added_ingredients_title)
        added_ingredients_header_layout.addWidget(added_ingredients_title)
        added_ingredients_header.setLayout(added_ingredients_header_layout)
        self.layout.addWidget(added_ingredients_header)

        # List for Added Ingredients
        self.added_ingredients = QWidget()
        self.added_ingredients_layout = QVBoxLayout()
        self.added_ingredients_layout.setContentsMargins(0, 0, 0, 0)
        self.added_ingredients_layout.setSpacing(0)
        self.added_ingredients.setLayout(self.added_ingredients_layout)
        self.layout.addWidget(self.added_ingredients)

        self.__list_added_ingredients()

        # Header for Search Ingredients section
        search_ingredients_header = QWidget()
        search_ingredients_header_layout = QHBoxLayout()
        search_ingredients_header_layout.setContentsMargins(0, 20, 0, 10)
        search_ingredients_title = QLabel("Search Ingredients:")
        style_h2(search_ingredients_title)
        search_ingredients_header_layout.addWidget(search_ingredients_title)
        search_ingredients_header_layout.addStretch(1)
        # SearchBar for ingredients
        self.search_bar = SearchBar(
            on_search=self.__list_found_ingredients,
            placeholder="Search Ingredients...",
        )
        search_ingredients_header_layout.addWidget(self.search_bar)
        search_ingredients_header.setLayout(search_ingredients_header_layout)
        self.layout.addWidget(search_ingredients_header)

        # List for Found Ingredients
        self.search_ingredients = QWidget()
        self.search_ingredients_layout = QVBoxLayout()
        self.search_ingredients_layout.setContentsMargins(0, 0, 0, 0)
        self.search_ingredients_layout.setSpacing(0)
        self.search_ingredients.setLayout(self.search_ingredients_layout)

        # Create a QScrollArea for Ingredients
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.search_ingredients)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMaximumHeight(180)
        self.layout.addWidget(self.scroll_area)
        # Set size policy to allow the scroll area to expand
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # List ingredients to start with
        self.__list_found_ingredients()

        self.setLayout(self.layout)

    def __list_found_ingredients(self, search: str = ""):
        clear_layout(self.search_ingredients_layout)

        ingredients = self.recipes_controller.list_ingredients(search)
        if ingredients:
            for ingredient in ingredients:
                is_added = ingredient['id'] in self.selected_ingredients
                quantity = self.selected_ingredients[ingredient['id']].get('quantity', 0.0) if is_added else 0.0
                self.search_ingredients_layout.addWidget(
                    IngredientsPickerIngredientItem(
                        ingredient=ingredient,
                        is_added=is_added,
                        quantity=quantity,
                        callback=self.__toggle_ingredient
                    )
                )
        else:
            label = QLabel("No ingredients found. Check search and try again.")
            style_h2(label)
            self.search_ingredients_layout.addWidget(label)

    def __list_added_ingredients(self):
        clear_layout(self.added_ingredients_layout)
        if self.selected_ingredients:
            for ingredient in self.selected_ingredients.values():
                self.added_ingredients_layout.addWidget(
                    IngredientsPickerIngredientItem(
                        ingredient=ingredient,
                        is_added=True,
                        quantity=ingredient.get("quantity", 0.0),
                        callback=self.__toggle_ingredient
                    )
                )
        else:
            label = QLabel("No added ingredients.")
            self.added_ingredients_layout.addWidget(label)

    def __toggle_ingredient(self, ingredient: dict, quantity: float):
        if ingredient['id'] in self.selected_ingredients:
            self.selected_ingredients.pop(ingredient['id'])
        else:
            # Update the ingredient dict with the new quantity
            ingredient['quantity'] = quantity
            self.selected_ingredients[ingredient['id']] = ingredient

        # Refresh both lists
        self.__list_found_ingredients(self.search_bar.q)
        self.__list_added_ingredients()
        # Update the selected ingredients as a list of (id, quantity) tuples
        self.set_ingredients([(ing['id'], ing['quantity']) for ing in self.selected_ingredients.values()])


class IngredientsPickerIngredientItem(QWidget):
    def __init__(
        self,
        ingredient: dict,
        is_added: bool,
        callback: Callable[[dict, float], None],
        quantity: float = None
    ):
        super().__init__()
        self.ingredient = ingredient
        self.is_added = is_added
        self.quantity = quantity if quantity is not None else 0.0
        self.callback = callback

        self.field = QLineEdit()
        self.field.setText(str(self.quantity) if self.quantity else "")
        regex = QRegExp("^[0-9]*\\.?[0-9]*$")
        validator = QRegExpValidator(regex)
        self.field.setReadOnly(is_added)
        self.field.setValidator(validator)
        self.field.setPlaceholderText("Quantity:")
        self.field.textChanged.connect(self.__update_value)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        layout.addWidget(QLabel(f"{ingredient['name']} ({ingredient['unit']})"))
        layout.addStretch(1)
        layout.addWidget(self.field)
        add_btn = QPushButton("Delete" if is_added else "Add")
        add_btn.clicked.connect(self.__handle_click)
        layout.addWidget(add_btn)
        self.setLayout(layout)

    def __update_value(self, new_value: str):
        try:
            self.quantity = float(new_value) if new_value else 0.0
        except ValueError:
            self.quantity = 0.0

    def __handle_click(self):
        if self.quantity is None or self.quantity == 0:
            return
        self.callback(self.ingredient, self.quantity)
