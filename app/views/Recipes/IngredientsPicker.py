from typing import Callable

from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy, QLineEdit

from app.controllers.RecipesController import RecipesController
from app.utils import clear_layout, style_h2
from app.views.SearchBar import SearchBar


class IngredientsPicker(QWidget):
    """A widget for selecting and managing ingredients with search and quantity input.

    Displays a list of added ingredients and a searchable list of available ingredients.
    Users can add or remove ingredients with quantities, and the selected ingredients are
    passed to a callback function as a list of (id, quantity) tuples.

    Attributes:
        selected_ingredients: Maps ingredient IDs to their details (id, name, unit, quantity).
        set_ingredients: Callback to update the parent with selected ingredients.
    """

    def __init__(self, ingredients: list[dict], set_ingredients: Callable[[list[tuple[int, float]]], None]):
        super().__init__()
        self.selected_ingredients = {ingredient['id']: ingredient for ingredient in ingredients}
        self.set_ingredients = set_ingredients
        self.recipes_controller = RecipesController()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        self.left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()

        # Header for Added Ingredients section
        added_ingredients_header = QWidget()
        added_ingredients_header_layout = QHBoxLayout()
        added_ingredients_header_layout.setContentsMargins(0, 10, 0, 10)
        added_ingredients_title = QLabel("Added Ingredients:")
        style_h2(added_ingredients_title)
        added_ingredients_header_layout.addWidget(added_ingredients_title)
        added_ingredients_header.setLayout(added_ingredients_header_layout)
        self.left_column.addWidget(added_ingredients_header)

        # List for Added Ingredients
        self.added_ingredients = QWidget()
        self.added_ingredients_layout = QVBoxLayout()
        self.added_ingredients_layout.setContentsMargins(0, 0, 0, 0)
        self.added_ingredients_layout.setSpacing(0)
        self.added_ingredients.setLayout(self.added_ingredients_layout)

        self.added_scroll_area = QScrollArea()
        self.added_scroll_area.setWidget(self.added_ingredients)
        self.added_scroll_area.setWidgetResizable(True)
        self.added_scroll_area.setMinimumHeight(180)
        self.added_scroll_area.setMaximumHeight(180)
        self.left_column.addWidget(self.added_scroll_area)
        self.added_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.left_column.addStretch(1)

        self.__list_added_ingredients()

        # Header for Search Ingredients section
        search_ingredients_header = QWidget()
        search_ingredients_header_layout = QHBoxLayout()
        search_ingredients_header_layout.setContentsMargins(0, 0, 0, 00)
        search_ingredients_title = QLabel("Search Ingredients:")
        style_h2(search_ingredients_title)
        search_ingredients_header_layout.addWidget(search_ingredients_title)
        search_ingredients_header_layout.addStretch(1)
        self.search_bar = SearchBar(
            on_search=self.__list_found_ingredients,
            placeholder="Search Ingredients...",
        )
        search_ingredients_header_layout.addWidget(self.search_bar)
        search_ingredients_header.setLayout(search_ingredients_header_layout)
        self.right_column.addWidget(search_ingredients_header)

        # List for Found Ingredients
        self.search_ingredients = QWidget()
        self.search_ingredients_layout = QVBoxLayout()
        self.search_ingredients_layout.setContentsMargins(0, 0, 0, 0)
        self.search_ingredients_layout.setSpacing(0)
        self.search_ingredients.setLayout(self.search_ingredients_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.search_ingredients)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(180)
        self.scroll_area.setMaximumHeight(180)
        self.right_column.addWidget(self.scroll_area)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.right_column.addStretch(1)

        self.__list_found_ingredients()

        self.layout.addLayout(self.left_column, 1)
        self.layout.addLayout(self.right_column, 1)

        self.setLayout(self.layout)

    def __list_found_ingredients(self, search: str = ""):
        """Populate the searchable ingredients list based on a search query.

        Args:
            search: Optional search string to filter ingredients. Defaults to empty string.
        """
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
        self.search_ingredients_layout.addStretch(1)

    def __list_added_ingredients(self):
        """Populate the list of added ingredients."""
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
        self.added_ingredients_layout.addStretch(1)

    def __toggle_ingredient(self, ingredient: dict, quantity: float):
        """Toggle an ingredient's selection state and update the parent.

        Args:
            ingredient: Dictionary containing ingredient details (id, name, unit, quantity).
            quantity: The quantity to associate with the ingredient.
        """
        if ingredient['id'] in self.selected_ingredients:
            self.selected_ingredients.pop(ingredient['id'])
        else:
            ingredient['quantity'] = quantity
            self.selected_ingredients[ingredient['id']] = ingredient

        self.__list_found_ingredients(self.search_bar.q)
        self.__list_added_ingredients()
        self.set_ingredients([(ing['id'], ing['quantity']) for ing in self.selected_ingredients.values()])


class IngredientsPickerIngredientItem(QWidget):
    """A widget representing a single ingredient with quantity input and add/delete button.

    Attributes:
        ingredient: The ingredient details (id, name, unit).
        is_added: Whether the ingredient is currently selected.
        quantity: The quantity of the ingredient.
        callback: Function to call when toggling the ingredient.
    """

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
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)
        layout.addWidget(QLabel(f"{ingredient['name']} ({ingredient['unit']})"))
        layout.addStretch(1)
        layout.addWidget(self.field)
        add_btn = QPushButton("Delete" if is_added else "Add")
        add_btn.clicked.connect(self.__handle_click)
        layout.addWidget(add_btn)
        self.setLayout(layout)

    def __update_value(self, new_value: str):
        """Update the quantity when the input field changes.

        Args:
            new_value: The new text entered in the quantity field.
        """
        try:
            self.quantity = float(new_value) if new_value else 0.0
        except ValueError:
            self.quantity = 0.0

    def __handle_click(self):
        """Handle the add/delete button click and invoke the callback."""
        if self.quantity is None or self.quantity == 0:
            return
        self.callback(self.ingredient, self.quantity)