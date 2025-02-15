from PyQt5.QtWidgets import QLabel

from app.controllers.NavigationController import NavigationController


def home_page_factory(**kwargs):
    return QLabel("Home page")

def recipes_page_factory(nav_controller: NavigationController, **kwargs):
    return QLabel("Recipes Page")

def recipe_detail_page_factory(nav_controller: NavigationController, recipe=None, **kwargs):
    return QLabel("Detail: " + recipe["name"])

def recipe_edit_page_factory(nav_controller: NavigationController, recipe=None, **kwargs):
    return QLabel("Edit: " + recipe["name"])