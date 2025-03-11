import itertools

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

        total_calories = 0

        for recipe_ingredient in recipe.recipe_ingredients:
            ingredient = recipe_ingredient.ingredient
            quantity = recipe_ingredient.quantity

            if ingredient.unit in ["g", "ml"]:
                calorie_per_unit = ingredient.calories / 100
            else:
                calorie_per_unit = ingredient.calories

            total_calories += calorie_per_unit * quantity

        return round(total_calories)

    def getRecipeProtein(self, recipe: Recipe) -> float:

        total_protein = 0

        for recipe_ingredient in recipe.recipe_ingredients:
            ingredient = recipe_ingredient.ingredient
            quantity = recipe_ingredient.quantity

            if ingredient.unit in ["g", "ml"]:
                protein_per_unit = ingredient.protein / 100
            else:
                protein_per_unit = ingredient.protein

            total_protein += protein_per_unit * quantity

        return round(total_protein, 2)

    def getRecommendedRecipes(self, tdee: int) -> str | list[dict]:
        all_recipes = self.recipes_controller.list_recipes()

        meal_combinations = list(itertools.combinations(all_recipes, 3))

        min_calories = tdee * 0.9
        max_calories = tdee * 1.1

        valid_meals = []

        for meals in meal_combinations:
            total_calories = sum(self.getRecipeCalories(meal) for meal in meals)

            if min_calories <= total_calories <= max_calories:
                total_protein = sum(self.getRecipeProtein(meal) for meal in meals)
                valid_meals.append((meals, total_protein))

        if not valid_meals:
            return "No combination of 3 meals found for recommended calorie intake."

        best_meals = max(valid_meals, key=lambda x: x[1])[0]

        return list(best_meals)

    def getBMI(self, weight: float, height: float) -> float:
         height_in_meters = height / 100
         bmi = weight / (height_in_meters ** 2)
         return round(bmi, 2)