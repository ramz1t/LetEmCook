from PyQt5.QtWidgets import QLabel

from app.controllers.NavigationController import NavigationController
from app.views.Notes.CreateNoteView import CreateNoteView
from app.views.Notes.NoteDetailView import NoteDetailView
from app.views.Notes.NoteEditView import NoteEditView
from app.views.Notes.NotesListView import NotesListView
from app.views.Recipes.CreateRecipeView import CreateRecipeView
from app.views.Recipes.RecipeDetailView import RecipeDetailView
from app.views.Recipes.RecipeEditView import RecipeEditView
from app.views.Recipes.RecipesListView import RecipesListView
from app.views.Planner.RecommendedRecipesView import RecommendedRecipesView
from app.views.Settings.SettingsView import SettingsView


def home_page_factory(**kwargs):
    return QLabel("Home page")

def recipes_page_factory(nav_controller: NavigationController, **kwargs):
    return RecipesListView(nav_controller=nav_controller, **kwargs)

def recipe_detail_page_factory(nav_controller: NavigationController, recipe=None, **kwargs):
    return RecipeDetailView(nav_controller=nav_controller, recipe=recipe)

def recipe_edit_page_factory(nav_controller: NavigationController, recipe=None, **kwargs):
    return RecipeEditView(nav_controller=nav_controller, recipe=recipe)

def recipe_create_page_factory(nav_controller: NavigationController, **kwargs):
    return CreateRecipeView(nav_controller=nav_controller)

def notes_page_factory(nav_controller: NavigationController, **kwargs):
    return NotesListView(nav_controller=nav_controller, **kwargs)

def note_detail_page_factory(nav_controller: NavigationController, note=None, **kwargs):
    return NoteDetailView(nav_controller=nav_controller, note=note)

def note_edit_page_factory(nav_controller: NavigationController, note=None, **kwargs):
    return NoteEditView(nav_controller=nav_controller, note=note)

def note_create_page_factory(nav_controller: NavigationController,**kwargs):
    return CreateNoteView(nav_controller=nav_controller)

def recommended_recipes_page_factory(nav_controller: NavigationController, **kwargs):
    return RecommendedRecipesView(nav_controller=nav_controller)

def settings_page_factory(nav_controller: NavigationController, **kwargs):
    return SettingsView(nav_controller=nav_controller)