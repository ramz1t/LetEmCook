from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

from app.controllers.NavigationController import NavigationController
from app.enums.route import Route


class RecipesListItemView(QWidget):
    def __init__(self, recipe: dict, nav_controller: NavigationController):
        super().__init__()
        self.recipe = recipe
        self.nav_controller = nav_controller

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignVCenter)

        # ID label
        self.id_label = QLabel(str(recipe['id']))
        self.id_label.setStyleSheet("""
            color: gray;
            font-weight: semibold;
            font-size: 14px;
        """)

        # Name label
        self.name_label = QLabel(recipe["name"])
        self.name_label.setStyleSheet("""
            font-weight: bold;
            font-size: 16px;
        """)

        # Ingredients count label
        self.recipes_count_label_text = ""
        recipes_count = len(recipe["ingredients"])
        if recipes_count > 1:
            self.recipes_count_label_text = f"{recipes_count} ingredients"
        elif recipes_count == 1:
            self.recipes_count_label_text = f"1 ingredient"
        else:
            self.recipes_count_label_text = "No ingredients"
        self.recipes_count_label = QLabel(self.recipes_count_label_text)
        self.recipes_count_label.setStyleSheet("""
            color: darkgray;
            font-weight: semibold;
            font-size: 14px;
        """)

        # View details button
        self.view_details_btn = QPushButton("View Details")
        self.view_details_btn.clicked.connect(lambda: self.nav_controller.navigate(Route.RECIPE_DETAIL, recipe=self.recipe))

        self.layout.addWidget(self.id_label)
        self.layout.addWidget(self.name_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.recipes_count_label)
        self.layout.addWidget(self.view_details_btn)

        self.setLayout(self.layout)