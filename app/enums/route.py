from enum import Enum, auto

class Route(Enum):
    HOME = auto()
    RECIPES = auto()
    RECIPE_DETAIL = auto()
    RECIPE_EDIT = auto()
    RECIPE_CREATE = auto()
    NOTES = auto()
    NOTE_DETAIL = auto()
    NOTE_EDIT = auto()
    NOTE_CREATE = auto()
    RECOMMENDATIONS = auto()
    SETTINGS = auto()
    # Add new routes here if needed
