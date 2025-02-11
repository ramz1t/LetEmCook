from typing import Tuple, List
from app.models import session_scope, Recipe, RecipeIngredient, Ingredient


class RecipesController:

    # Create recipe

    # Get all recipes (can be filtered by name)

    # Edit recipe by id and dict of changes
    def update(self, id: int, ingredients: List[Tuple[int, int]], **kwargs) -> Recipe | None:
        with session_scope() as session:
            recipe = session.query(Recipe).filter_by(id=id).first()
            if recipe:
                recipe.update(**kwargs)
                session.query(RecipeIngredient).filter_by(recipe_id=id).delete()
                for ingredient_id, quantity in ingredients:
                    ingredient = session.query(Ingredient).filter_by(id=ingredient_id).first()
                    recipe_ingredient = RecipeIngredient(recipe=recipe, ingredient=ingredient, quantity=quantity)
                    session.add(recipe_ingredient)
                return recipe
            return None

    # Delete recipe

    pass
