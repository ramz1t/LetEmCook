from app.controllers.RecipesController import RecipesController
from app.enums.activity_type import ActivityType
from app.enums.goal import Goal
from app.models import Recipe


class NutritionController:
    def __init__(self):
        self.recipes_controller = RecipesController()

    def getBMR(self, weight: float, height: float, age: int, gender: str) -> float:
        if gender == "female":
            return (weight * 10) + (height * 6.25) - (age * 5) - 161
        elif gender == "male":
            return (weight * 10) + (height * 6.25) - (age * 5) + 5
        else:
            raise ValueError("Gender is not male or female.")

    def getTDEE(self, weight: float, height: float, age: int, gender: str, activity_type: ActivityType, goal: Goal) -> int:
        bmr = self.getBMR(weight, height, age, gender)

        if not isinstance(activity_type, ActivityType):
            raise ValueError("Invalid activity type.")
        if not isinstance(goal, Goal):
            raise ValueError("Invalid goal type.")

        tdee = bmr * activity_type.value
        tdee += goal.value

        return round(tdee)

    def getRecipeCalories(self, recipe: Recipe) -> int:
        total_calories = sum(
            recipe_ingredient.ingredient.calories * recipe_ingredient.quantity
            for recipe_ingredient in recipe.recipe_ingredients
        )
        return round(total_calories)

    def getRecommendedRecipes(self, tdee: int) -> list[Recipe]:
        pass

    def getBMI(self, weight: float, height: float) -> float:
         height_in_meters = height / 100
         bmi = weight / (height_in_meters ** 2)
         return round(bmi, 2)