from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QHBoxLayout, QSizePolicy, QDialog
from PyQt5.QtCore import Qt
from sqlalchemy.orm.sync import clear

from app.controllers.NutritionController import NutritionController
from app.controllers.StorageManager import StorageManager
from app.enums.activity_type import ActivityType
from app.enums.goal import Goal
from app.enums.route import Route
from app.controllers.NavigationController import NavigationController
from app.enums.storage import StorageKey
from app.utils import clear_layout, style_h2
from app.views.CustomDialog import CustomDialog
from app.views.Recipes.RecipesListItemView import RecipesListItemView
from app.views.TopBar import TopBar
from app.views.Divider import Divider


class RecommendedRecipesView(QWidget):
    def __init__(self, nav_controller: NavigationController):
        super().__init__()

        self.nav_controller = nav_controller
        self.nutrition_controller = NutritionController()

        # Goal selection dropdown
        self.goal_layout = QHBoxLayout()
        self.goal_label = QLabel("Goal:")
        self.goal_dropdown = QComboBox(self)
        self.goal_dropdown.addItems([goal.name for goal in Goal])
        self.goal_dropdown.setCurrentText(StorageManager.get_value(StorageKey.Goal.value, ""))
        self.goal_layout.addWidget(self.goal_label)
        self.goal_layout.addWidget(self.goal_dropdown)
        self.goal_widget = QWidget()
        self.goal_widget.setLayout(self.goal_layout)

        # Recommend button
        self.recommend_button = QPushButton("Recommend")
        self.recommend_button.clicked.connect(self.__get_recommendations)

        # Activity type selection dropdown
        self.activity_type_layout = QHBoxLayout()
        self.activity_type_label = QLabel("Activity type:")
        self.activity_type_dropdown = QComboBox(self)
        self.activity_type_dropdown.addItems([each.name for each in ActivityType])
        self.activity_type_dropdown.setCurrentText(StorageManager.get_value(StorageKey.ActivityType.value, ""))
        self.activity_type_layout.addWidget(self.activity_type_label)
        self.activity_type_layout.addWidget(self.activity_type_dropdown)
        self.activity_type_widget = QWidget()
        self.activity_type_widget.setLayout(self.activity_type_layout)

        # Layout setup
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Set page TopBar
        self.layout.addWidget(
            TopBar(
                title="Planner",
                nav_controller=nav_controller,
                actions=[self.goal_widget, self.activity_type_widget, self.recommend_button],
                is_root_view=True,
            )
        )
        # Add small divider below TopBar
        self.layout.addWidget(Divider())

        # List widget to display recommended recipes
        self.recipes_list = QWidget()  # Using QWidget instead of QListWidget for custom layout
        self.recipes_layout = QVBoxLayout()  # Use QVBoxLayout to stack recipes vertically
        self.recipes_list.setLayout(self.recipes_layout)
        self.recipes_list.setMinimumHeight(400)
        self.recipes_layout.setContentsMargins(0, 0, 0, 0)
        self.recipes_layout.setSpacing(0)
        self.layout.addWidget(self.recipes_list)

        # Set the layout
        self.setLayout(self.layout)

    def __get_recommendations(self):
        """Fetches and displays recommended recipes."""
        goal_value = self.goal_dropdown.currentText()
        activity_type_value = self.activity_type_dropdown.currentText()

        selected_goal = Goal[goal_value]
        selected_activity_type = ActivityType[activity_type_value]

        StorageManager.set_value(StorageKey.Goal.value, goal_value)
        StorageManager.set_value(StorageKey.ActivityType.value, activity_type_value)

        weight = StorageManager.get_value(StorageKey.CurrentWeight.value, None)
        height = StorageManager.get_value(StorageKey.Height.value, None)
        age = StorageManager.get_value(StorageKey.CurrentWeight.value, None)
        gender = StorageManager.get_value(StorageKey.Sex.value, None)

        if not weight or not height or not age or not gender:
            dialog = CustomDialog(
                "Insufficient data",
                "We are missing some info about you and are unable to suggest recipes. Do you want to go to settings?",
                "Yes"
            )
            if dialog.exec_() == QDialog.Accepted:
                self.nav_controller.navigate(Route.SETTINGS)
                return

        tdee = self.nutrition_controller.get_TDEE(
            weight=float(weight),
            height=float(height),
            age=int(age),
            gender=gender.lower(),
            activity_type=selected_activity_type,
            goal=selected_goal
        )
        recommended_recipes = self.nutrition_controller.get_recommended_recipes(tdee)

        clear_layout(self.recipes_layout)

        self.subheader = QWidget()
        self.subheader_layout = QHBoxLayout()
        self.subheader_layout.setContentsMargins(20, 10, 20, 10)
        self.subheader.setLayout(self.subheader_layout)

        self.tdee_label = QLabel(f"Your estimated daily consumption: {tdee}kcal")
        style_h2(self.tdee_label)

        self.subheader_layout.addWidget(self.tdee_label)
        self.subheader_layout.addStretch(1)

        self.recipes_layout.addWidget(self.subheader)
        self.recipes_layout.addWidget(Divider())

        if not recommended_recipes or not isinstance(recommended_recipes, list):
            no_recipes_label = QLabel("No combination of 3 meals found for recommended calorie intake.") # TODO: replace with NoContentView
            self.recipes_layout.addWidget(no_recipes_label)
        else:
            for recipe in recommended_recipes:
                recipe_item = RecipesListItemView(recipe=recipe, nav_controller=self.nav_controller)
                self.recipes_layout.addWidget(recipe_item)
                self.recipes_layout.addWidget(Divider(opacity=0.3))
            self.total_cals = sum(self.nutrition_controller.get_recipe_calories(recipe) for recipe in recommended_recipes)
            self.total_cals_label = QLabel(f"Total calorie intake: {self.total_cals}kcal")
            style_h2(self.total_cals_label)
            self.total_cals_label.setContentsMargins(20, 10, 0, 10)
            self.subheader_layout.addWidget(self.total_cals_label)

        self.recipes_layout.addStretch()
