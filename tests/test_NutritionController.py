import pytest
from unittest.mock import MagicMock
from app.controllers.NutritionController import NutritionController
from app.enums.activity_type import ActivityType
from app.enums.goal import Goal
from app.models import Recipe, Ingredient, RecipeIngredient

@pytest.fixture
def nutrition_controller():
    controller = NutritionController()
    controller.recipes_controller = MagicMock()
    return controller

def test_get_BMR_female(nutrition_controller):
    weight = 60
    height = 165
    age = 30
    gender = "female"
    expected_bmr = (weight * 10) + (height * 6.25) - (age * 5) - 161
    assert nutrition_controller.get_BMR(weight, height, age, gender) == expected_bmr

def test_getBMR_male(nutrition_controller):
    weight = 70
    height = 175
    age = 25
    gender = "male"
    expected_bmr = (weight * 10) + (height * 6.25) - (age * 5) + 5
    assert nutrition_controller.get_BMR(weight, height, age, gender) == expected_bmr

def test_get_BMR_invalid_gender(nutrition_controller):
    with pytest.raises(ValueError):
        nutrition_controller.get_BMR(60, 165, 30, "other")

def test_get_TDEE(nutrition_controller):
    weight = 60
    height = 165
    age = 30
    gender = "female"
    activity_type = ActivityType.Moderately_active
    goal = Goal.Maintain
    bmr = nutrition_controller.get_BMR(weight, height, age, gender)
    expected_tdee = round(bmr * activity_type.value + goal.value)
    assert nutrition_controller.get_TDEE(weight, height, age, gender, activity_type, goal) == expected_tdee

def test_get_TDEE_invalid_activity_type(nutrition_controller):
    with pytest.raises(ValueError):
        nutrition_controller.get_TDEE(60, 165, 30, "female", "invalid_activity", Goal.Maintain)

def test_get_TDEE_invalid_goal(nutrition_controller):
    with pytest.raises(ValueError):
        nutrition_controller.get_TDEE(60, 165, 30, "female", ActivityType.Moderately_active, "invalid_goal")

def test_get_recipe_calories(nutrition_controller):
    ingredient1 = Ingredient(name="Chicken", calories=165, protein=31, unit="g")
    ingredient2 = Ingredient(name="Rice", calories=130, protein=2.7, unit="g")
    recipe_ingredient1 = RecipeIngredient(ingredient=ingredient1, quantity=200)
    recipe_ingredient2 = RecipeIngredient(ingredient=ingredient2, quantity=150)
    recipe = Recipe(recipe_ingredients=[recipe_ingredient1, recipe_ingredient2])
    expected_calories = round((ingredient1.calories / 100 * 200) + (ingredient2.calories / 100 * 150))
    assert nutrition_controller.get_recipe_calories(recipe.to_dict()) == expected_calories

def test_get_recipe_protein(nutrition_controller):
    ingredient1 = Ingredient(name="Chicken", calories=165, protein=31, unit="g")
    ingredient2 = Ingredient(name="Rice", calories=130, protein=2.7, unit="g")
    recipe_ingredient1 = RecipeIngredient(ingredient=ingredient1, quantity=200)
    recipe_ingredient2 = RecipeIngredient(ingredient=ingredient2, quantity=150)
    recipe = Recipe(recipe_ingredients=[recipe_ingredient1, recipe_ingredient2])
    expected_protein = round((ingredient1.protein / 100 * 200) + (ingredient2.protein / 100 * 150), 2)
    assert nutrition_controller.get_recipe_protein(recipe.to_dict()) == expected_protein

def test_get_recommended_recipes(nutrition_controller):
    ingredient1 = Ingredient(calories=100, protein=10, unit="g")
    ingredient2 = Ingredient(calories=200, protein=20, unit="g")
    ingredient3 = Ingredient(calories=300, protein=30, unit="g")
    ingredient4 = Ingredient(calories=600, protein=30, unit="g")

    recipe_ingredient1 = RecipeIngredient(ingredient=ingredient1, quantity=100)
    recipe_ingredient2 = RecipeIngredient(ingredient=ingredient2, quantity=100)
    recipe_ingredient3 = RecipeIngredient(ingredient=ingredient3, quantity=100)
    recipe_ingredient4 = RecipeIngredient(ingredient=ingredient4, quantity=100)

    recipe1 = Recipe(recipe_ingredients=[recipe_ingredient1])
    recipe2 = Recipe(recipe_ingredients=[recipe_ingredient2])
    recipe3 = Recipe(recipe_ingredients=[recipe_ingredient3])
    recipe4 = Recipe(recipe_ingredients=[recipe_ingredient4])

    nutrition_controller.recipes_controller.list_recipes = lambda: [recipe1.to_dict(), recipe2.to_dict(), recipe3.to_dict(), recipe4.to_dict()]

    tdee = 600
    expected_recipes = [recipe1.to_dict(), recipe2.to_dict(), recipe3.to_dict()]

    assert nutrition_controller.get_recommended_recipes(tdee) == expected_recipes

def test_get_BMI(nutrition_controller):
    weight = 70
    height = 175
    expected_bmi = round(weight / ((height / 100) ** 2), 2)
    assert nutrition_controller.get_BMI(weight, height) == expected_bmi
