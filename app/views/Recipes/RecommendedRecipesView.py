from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QListWidget, QListWidgetItem
from app.controllers.NutritionController import NutritionController
from app.enums.activity_type import ActivityType
from app.enums.goal import Goal
from app.enums.route import Route
from app.views.Recipes.RecipesListItemView import RecipesListItemView  # Reusing this
from app.controllers.NavigationController import NavigationController
from app.views.TopBar import TopBar
from app.views.Divider import Divider


# #     goal button, activity type button, recommendations button
        ## change it with just qwidget, layout for this list, qvboxlayout, helper function to clean this list, pass clear layout function to the layout.


class RecommendedRecipesView(QWidget):
    def __init__(self, nav_controller: NavigationController):
        super().__init__()

        self.nav_controller = nav_controller
        self.nutrition_controller = NutritionController()

        # Goal selection dropdown
        self.goal_dropdown = QComboBox(self)
        self.goal_dropdown.addItems([goal.name for goal in Goal])

        # Recommend button
        self.recommend_button = QPushButton("Recommend")
        self.recommend_button.clicked.connect(self.get_recommendations)

        # Activity type selection dropdown
        self.activity_type_dropdown = QComboBox(self)
        self.activity_type_dropdown.addItems([each.name.replace("_", " ").title() for each in ActivityType])

        # Layout setup
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Set page TopBar
        self.layout.addWidget(
            TopBar(
                title="Recommended Recipes",
                nav_controller=nav_controller,
                actions=[self.goal_dropdown, self.activity_type_dropdown, self.recommend_button],
                is_root_view=True,
            )
        )
        # Add small divider below TopBar
        self.layout.addWidget(Divider())

        # List widget to display recommended recipes
        self.recipes_list = QListWidget(self)
        self.layout.addWidget(self.recipes_list)

        # Set the layout
        self.setLayout(self.layout)

    def get_recommendations(self):
        """Fetches and displays recommended recipes."""
        selected_goal = Goal[self.goal_dropdown.currentText()]

        # Hardcoded body values (Replace with StorageController later)
        weight, height, age, gender = 70, 175, 25, "male"
        activity_type = ActivityType.Sedentary

        # Calculate TDEE and get recommended recipes
        tdee = self.nutrition_controller.getTDEE(weight, height, age, gender, activity_type, selected_goal)
        recommended_recipes = self.nutrition_controller.getRecommendedRecipes(tdee)

        # Clear previous results
        self.recipes_list.clear()

        if isinstance(recommended_recipes, list):
            for recipe in recommended_recipes:
                item = QListWidgetItem(self.recipes_list)
                recipe_view = RecipesListItemView(recipe, self.nav_controller)
                item.setSizeHint(recipe_view.sizeHint())
                self.recipes_list.addItem(item)
                self.recipes_list.setItemWidget(item, recipe_view)
        else:
            self.recipes_list.addItem("No combination of 3 meals found for recommended calorie intake.")