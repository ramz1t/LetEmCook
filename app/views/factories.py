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
    # Since the app's window size is fixed, some lines need a forced <br> to stay in frame and for the "text-align: center" being correct.
    introduction = QLabel('''
    <div style="margin-left: 15px;">
    <br>
    <p style="text-align: center; font-size: 30px;">
    <b>Welcome to 
    </p>
    <p style="text-align: center; font-size: 60px;">
    <b>Let'EmCook</b>
    </p>
    <br>
    <p style="font-size: 15px;">The goal of this app is to help you manage your diet so you can keep a better track of the nutrients and calories you <br> eat to make you feel better.</p>

    <hr>
    <p style="font-size: 15px;">
    <b>|RECIPES|</b>: Here you can create, edit and delete your recipes.<br>
    <b>|NOTES|</b>: Create any notes you need, talk about your recipes, how they make you feel, or experiences you have.<br>
    <b>|PLANNER|</b>: Get meal suggestions based on your activity to reach a recommended calorie level.<br>
    <b>|SETTINGS|</b>: Do not forget to update your body metrics and age as time goes by!<br>
    </p>
    <hr>

    <p style="font-size: 15px;">
    <b>Remember:</b><br>
    - Having enough energy helps you stay on track with your routine. Carbohydrates offer a stable energy source while sugars may cause a <br> &nbsp; fluctuation in energy levels.<br>
    - Foods rich in tryptophan (turkey, bananas, dairy) help produce serotonin, the "happiness hormone."<br>
    - Stress and Anxiety Reduction: Omega-3 fatty acids (fish, nuts) and antioxidants (fruits, vegetables) can help lower stress and improve <br> &nbsp; emotional well-being.<br>
    - Tracking your mood and your feelings with recipes will help you achieve the diet you need to confront everyday plans. Looking back at your <br> &nbsp; notes can give you valuable insights to improve your diet and well-being.<br>
    </p>
    <hr>
    <p style="font-size: 15px;"><b>This app has been created by:</b>
    <ul>
        <li><a href="https://github.com/ramz1t">Timur Ramazanov</a> (main repository)</li>
        <li><a href="https://github.com/ayahassaad">Ayah Assaad</a></li>
        <li><a href="https://github.com/skgmsj">Sebastian Karström</a></li>
        <li><a href="https://github.com/mavagoncalves">Maria Valentina Gonçalves Rojas</a></li>
        <li><a href="https://github.com/robrodres">Roberto Rodríguez Espejo</a></li>
    </ul>
    </p>
    <br>
    </dv>
    ''')
    # This makes our url´s clickable
    introduction.setOpenExternalLinks(True)

    return introduction

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