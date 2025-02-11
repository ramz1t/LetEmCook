import os

from PyQt5.QtWidgets import QLabel

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

NAVIGATION = [
    {
        "icon": "resources/images/icons/home.png",
        "title": "Home",
        "view_factory": lambda: QLabel("HOME_PAGE")
    },
    {
        "icon": "resources/images/icons/home.png",
        "title": "Recipes",
        "view_factory": lambda: QLabel("RECIPES_PAGE")
    }
]
