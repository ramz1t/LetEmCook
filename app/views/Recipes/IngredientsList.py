from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout

from app.utils import get_recipes_count_label
from app.views.Divider import Divider
from app.views.InfoContainer import InfoContainer


class IngredientsList(QWidget):
    def __init__(self, ingredients: list[dict]):
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

        nutrition_info_label = None

        if ingredients:
            # Header with ingredients count
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

            ingredients_list_layout.addWidget(self.__create_title_row())
            ingredients_list_layout.addWidget(Divider(opacity=0.7))

            for index, ingredient in enumerate(ingredients):
                ingredients_list_layout.addWidget(self.__create_ingredient_item_view(ingredient))
                if index < len(ingredients) - 1:
                    ingredients_list_layout.addWidget(Divider(opacity=0.3))

            nutrition_info_label = QLabel("Nutrition per 100g/ml or 1pc\nIngredients per 1 portion")
            nutrition_info_label.setStyleSheet("font-size: 12px; color: gray;")
            nutrition_info_label.setContentsMargins(10, 10, 10, 10)

        else:
            ingredients_list_layout.addWidget(QLabel("No ingredients"))  # TODO: replace with NoContentView

        layout.addWidget(InfoContainer(ingredients_list))

        if nutrition_info_label:
            layout.addWidget(nutrition_info_label)

    def __create_ingredient_item_view(self, ingredient: dict) -> QWidget:
        ingredient_view = QWidget()
        ingredient_layout = self.__create_ingredient_row_layout()

        # Name label
        name_label = QLabel(ingredient["name"])
        name_label.setStyleSheet("""
                font-weight: bold;
                font-size: 14px;
            """)
        ingredient_layout.addWidget(name_label, 0, 0)

        # Calories label
        ingredient_layout.addWidget(self.__create_nutrition_label(f"{int(ingredient['calories'])} kcal"), 0, 1)

        # Fats label
        ingredient_layout.addWidget(self.__create_nutrition_label(f"{int(ingredient['fats'])}g"), 0, 2)

        # Sugars label
        ingredient_layout.addWidget(self.__create_nutrition_label(f"{int(ingredient['sugars'])}g"), 0, 3)

        # Carbs label
        ingredient_layout.addWidget(self.__create_nutrition_label(f"{int(ingredient['carbohydrates'])}g"), 0, 4)

        # Protein label
        ingredient_layout.addWidget(self.__create_nutrition_label(f"{int(ingredient['protein'])}g"), 0, 5)

        # Quantity label
        ingredient_layout.addWidget(self.__create_nutrition_label(f"{ingredient['quantity']}{ingredient['unit']}"), 0, 6)

        ingredient_view.setLayout(ingredient_layout)
        return ingredient_view

    def __create_nutrition_label(self, s: float | str):
        nutrition_label = QLabel(str(s))
        nutrition_label.setStyleSheet("""
            color: gray;
            font-weight: semibold;
            font-size: 12px;
        """)
        return nutrition_label

    def __create_title_row(self):
        title_row = QWidget()

        title_row_layout = self.__create_ingredient_row_layout()

        title_row_layout.addWidget(QLabel("Calories"), 0, 1)
        title_row_layout.addWidget(QLabel("Fats"), 0, 2)
        title_row_layout.addWidget(QLabel("Sugars"), 0, 3)
        title_row_layout.addWidget(QLabel("Carbs"), 0, 4)
        title_row_layout.addWidget(QLabel("Protein"), 0, 5)
        title_row_layout.addWidget(QLabel("Quantity"), 0, 6)

        title_row.setLayout(title_row_layout)
        return title_row

    def __create_ingredient_row_layout(self) -> QGridLayout:
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 1)
        layout.setColumnStretch(5, 1)
        layout.setColumnStretch(6, 1)
        return layout
