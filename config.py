import os
from app.enums.route import Route

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

NAVIGATION = [
    {
        "icon": "\U0001F3E0",
        "title": "Home",
        "route": Route.HOME
    },
    {
        "icon": "\U0001F373",
        "title": "Recipes",
        "route": Route.RECIPES
    },
    {
        "icon": "\U0001F4DD",
        "title": "Notes",
        "route": Route.NOTES
    }
]
