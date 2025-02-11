from typing import List, Tuple

from app.models import session_scope, Recipe, Ingredient, RecipeIngredient


class RecipesController:
    def create(self, ingredients: List[Tuple[int, int]], **kwargs) -> Recipe:
        with session_scope() as session:
            recipe = Recipe(**kwargs)
            recipe_ingredients = []
            for ingredient in ingredients:
                db_ingredient = session.query(Ingredient).filter_by(id=ingredient[0]).first()
                if db_ingredient is None: continue
                recipe_ingredient = RecipeIngredient(recipe=recipe, ingredient=db_ingredient, quantity=ingredient[1])
                recipe_ingredients.append(recipe_ingredient)
            session.add(recipe)
            session.add_all(recipe_ingredients)
            return recipe

    # Get all recipes (can be filtered by name)
    def list(self, search: str = "", ) -> List[Recipe]:
        with session_scope() as session:
            if search:
                search_term = f'%{search}%'
                recipes = session.query(Recipe).filter(Recipe.name.ilike(search_term)) | session.query(Recipe).filter(Recipe.description.ilike(search_term)).all()
            else:
                recipes = session.query(Recipe).all()
            return recipes


    # Edit recipe by id and dict of changes

    # Delete recipe

    pass
