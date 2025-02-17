from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from app.utils import get_recipes_count_label
from app.views.Divider import Divider
from app.views.InfoContainer import InfoContainer


class IngredientsList(QWidget):
    def __init__(self, ingredients: list[dict], set_sorting: Callable):
        super().__init__()
        # All ingredients area (header and list)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 0, 20, 20)
        layout.setSpacing(0)
        self.setLayout(layout)

        # List of ingredients
        ingredients_list = QWidget()
        ingredients_list_layout = QVBoxLayout()
        ingredients_list_layout.setContentsMargins(0, 0, 0, 0)
        ingredients_list_layout.setSpacing(0)
        ingredients_list.setLayout(ingredients_list_layout)

        if ingredients:
            # Header with ingredients count and sorting picker
            header = QWidget()
            header_layout = QHBoxLayout()
            header_layout.setContentsMargins(10, 10, 10, 10)
            header_layout.setSpacing(0)
            header_layout.setAlignment(Qt.AlignVCenter)
            count_label = QLabel(get_recipes_count_label(len(ingredients)))
            count_label.setStyleSheet("font-size: 12px; color: gray;")
            header_layout.addWidget(count_label)
            header.setLayout(header_layout)

            layout.addWidget(header)

            for index, ingredient in enumerate(ingredients):
                ingredients_list_layout.addWidget(self.__create_ingredient_item_view(ingredient))
                if index < len(ingredients) - 1:
                    ingredients_list_layout.addWidget(Divider(opacity=0.3))
        else:
            ingredients_list_layout.addWidget(QLabel("No ingredients"))  # TODO: replace with NoContentView

        layout.addWidget(InfoContainer(ingredients_list))

    def __create_ingredient_item_view(self, ingredient: dict) -> QWidget:
        ingredient_view = QWidget()
        ingredient_layout = QHBoxLayout()
        ingredient_layout.setContentsMargins(10, 10, 10, 10)
        ingredient_layout.setSpacing(0)
        ingredient_layout.setAlignment(Qt.AlignVCenter)

        name_label = QLabel(ingredient["name"])
        name_label.setStyleSheet("""
            font-weight: bold;
            font-size: 14px;
        """)

        quantity_label = QLabel(f"{str(ingredient['quantity'])} {ingredient['unit']}")
        quantity_label.setStyleSheet("""
            color: gray;
            font-weight: semibold;
            font-size: 12px;
        """)

        ingredient_layout.addWidget(name_label)
        ingredient_layout.addStretch(1)
        ingredient_layout.addWidget(quantity_label)

        ingredient_view.setLayout(ingredient_layout)
        return ingredient_view