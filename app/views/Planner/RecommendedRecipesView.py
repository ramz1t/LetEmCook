from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from sqlalchemy.orm.sync import clear

from app.controllers.NutritionController import NutritionController
from app.enums.activity_type import ActivityType
from app.enums.goal import Goal
from app.enums.route import Route
from app.controllers.NavigationController import NavigationController
from app.utils import clear_layout
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
        self.goal_layout.addWidget(self.goal_label)
        self.goal_layout.addWidget(self.goal_dropdown)
        self.goal_widget = QWidget()
        self.goal_widget.setLayout(self.goal_layout)

        # Recommend button
        self.recommend_button = QPushButton("Recommend")
        self.recommend_button.clicked.connect(self.get_recommendations)

        # Activity type selection dropdown
        self.activity_type_layout = QHBoxLayout()
        self.activity_type_label = QLabel("Activity type:")
        self.activity_type_dropdown = QComboBox(self)
        self.activity_type_dropdown.addItems([each.name.replace("_", " ").title() for each in ActivityType])
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
        self.layout.addWidget(self.recipes_list)

        # Set the layout
        self.setLayout(self.layout)

    def get_recommendations(self):
        """Fetches and displays recommended recipes."""
        selected_goal = Goal[self.goal_dropdown.currentText()]

        # Hardcoded body values (Replace with StorageController later)
        weight, height, age, gender = 70, 175, 25, "male"
        activity_type = ActivityType.Sedentary # change when user uses dropdown

        # Calculate TDEE and get recommended recipes
        tdee = self.nutrition_controller.get_TDEE(weight, height, age, gender, activity_type, selected_goal)
        recommended_recipes = self.nutrition_controller.get_recommended_recipes(tdee)

        # Clear previous results
        clear_layout(self.recipes_layout)


        if not recommended_recipes or not isinstance(recommended_recipes, list):
            no_recipes_label = QLabel("No combination of 3 meals found for recommended calorie intake.") # TODO: replace with NoContentView
            self.recipes_layout.addWidget(no_recipes_label)
            return  # Stop execution

        for recipe in recommended_recipes:
            recipe_item = RecipesListItemView(recipe=recipe, nav_controller=self.nav_controller)


            self.recipes_layout.addWidget(recipe_item)

