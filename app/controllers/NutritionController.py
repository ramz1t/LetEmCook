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
        pass

    def getRecipeCalories(self, recipe: Recipe) -> int:
        pass

    def getRecommendedRecipes(self, tdee: int) -> list[Recipe]:
        pass

    def getBMI(self, weight: float, height: float) -> float:
        pass



