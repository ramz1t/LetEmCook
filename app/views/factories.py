from PyQt5.QtWidgets import QLabel

from app.controllers.NavigationController import NavigationController
from app.views.Recipes.CreateRecipeView import CreateRecipeView
from app.views.Recipes.RecipeDetailView import RecipeDetailView
from app.views.Recipes.RecipesListView import RecipesListView


def home_page_factory(**kwargs):
    return QLabel("Home page")

def recipes_page_factory(nav_controller: NavigationController, **kwargs):
    return RecipesListView(nav_controller=nav_controller, **kwargs)

def recipe_detail_page_factory(nav_controller: NavigationController, recipe=None, **kwargs):
    return RecipeDetailView(nav_controller=nav_controller, recipe=recipe)

def recipe_edit_page_factory(nav_controller: NavigationController, recipe=None, **kwargs):
    return QLabel("Edit: " + recipe["name"])

def recipe_create_page_factory(nav_controller: NavigationController, **kwargs):
    return CreateRecipeView(nav_controller=nav_controller)