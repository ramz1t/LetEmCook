from PyQt5.QtWidgets import QWidget, QFormLayout, QVBoxLayout, QPushButton, QMessageBox, QDialog

from app.controllers.NavigationController import NavigationController
from app.controllers.RecipesController import RecipesController
from app.enums.route import Route
from app.views.CustomDialog import CustomDialog
from app.views.Divider import Divider
from app.views.Recipes.RecipeForm import RecipeForm
from app.views.TopBar import TopBar


class RecipeEditView(QWidget):
    def __init__(self, recipe: dict, nav_controller: NavigationController):
        super().__init__()
        self.recipe = recipe
        self.nav_controller = nav_controller
        self.recipes_controller = RecipesController()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setStyleSheet("color: red;")
        self.delete_btn.clicked.connect(lambda: self.__show_confirmation_dialog())

        self.layout.addWidget(
            TopBar(
                title=f"Edit - {recipe['name']}",
                nav_controller=nav_controller,
                actions=[
                    self.delete_btn
                ]
            )
        )
        self.layout.addWidget(Divider())

        self.layout.addWidget(RecipeForm(self.__update_recipe, self.recipe))

        self.setLayout(self.layout)

    def __show_confirmation_dialog(self):
        dialog = CustomDialog(
            "Would you like to delete this recipe?",
            "This recipe will be deleted from the list. This action cannot be undone.",
            "Delete"
        )

        if dialog.exec_() == QDialog.Accepted:
            self.__delete_recipe()

    def __delete_recipe(self):
        deleted = self.recipes_controller.delete(id=self.recipe["id"])
        if deleted:
            self.nav_controller.navigate(Route.RECIPES)

    def __update_recipe(self, data: dict):
        new_recipe = self.recipes_controller.update(self.recipe['id'], **data)
        if new_recipe:
            self.nav_controller.navigate(Route.RECIPE_DETAIL, recipe=new_recipe)
