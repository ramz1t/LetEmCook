from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout

from app.controllers.NavigationController import NavigationController
from app.enums.route import Route
from app.views.Divider import Divider
from app.views.InfoContainer import InfoContainer
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

        # Create ingredients list
        self.ingredients_box = QWidget()
        self.ingredients_layout = QVBoxLayout()
        self.ingredients_layout.setContentsMargins(0, 0, 0, 0)
        self.ingredients_layout.setSpacing(0)

        ingredients = recipe["ingredients"]
        if ingredients:
            for index, ingredient in enumerate(ingredients, start=1):
                self.ingredients_layout.addWidget(self._create_ingredient_view(index, ingredient))
                if index < len(ingredients):
                    self.ingredients_layout.addWidget(Divider(opacity=0.3, margin=20))
        else:
            self.ingredients_layout.addWidget(QLabel("No ingredients")) # TODO: replace with NoContentView

        self.ingredients_box.setLayout(self.ingredients_layout)
        self.layout.addWidget(InfoContainer(self.ingredients_box, margin="0 20px"))

        self.setLayout(self.layout)

    def _create_ingredient_view(self, index: int, ingredient: dict) -> QWidget:
        ingredient_view = QWidget()
        ingredient_layout = QHBoxLayout()
        ingredient_layout.setContentsMargins(10, 10, 10, 10)
        ingredient_layout.setSpacing(0)
        ingredient_layout.setAlignment(Qt.AlignVCenter)

        index_label = QLabel(str(index))
        index_label.setStyleSheet("""
            color: gray;
            font-weight: semibold;
            font-size: 12px;
            padding: 0;
        """)
        index_label.setMinimumWidth(60)

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

        ingredient_layout.addWidget(index_label)
        ingredient_layout.addWidget(name_label)
        ingredient_layout.addStretch(1)
        ingredient_layout.addWidget(quantity_label)

        ingredient_view.setLayout(ingredient_layout)
        return ingredient_view
