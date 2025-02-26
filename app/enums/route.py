from enum import Enum, auto

class Route(Enum):
    HOME = auto()
    RECIPES = auto()
    RECIPE_DETAIL = auto()
    RECIPE_EDIT = auto()
    RECIPE_CREATE = auto()
    NOTES = auto()
    NOTE_DETAIL = auto()
    # Add new routes here if needed
