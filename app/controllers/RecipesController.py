from sqlalchemy.orm import Session

from app.models import session_scope, Recipe, Ingredient, RecipeIngredient


class RecipesController:
    def create(self, ingredients: list[tuple[int, int]], **kwargs) -> Recipe:
        with session_scope() as session:
            recipe = Recipe(**kwargs)
            session.add(recipe)
            self._add_recipe_ingredients(recipe, ingredients, session)
            return recipe

    def list_recipes(self, search: str = str()) -> list[Recipe]:
        with session_scope() as session:
            if search:
                search_term = f'%{search}%'
                recipes = session.query(Recipe).filter(
                    (Recipe.name.ilike(search_term)) | (Recipe.description.ilike(search_term))
                ).all()
            else:
                recipes = session.query(Recipe).all()
            return recipes

    def update(self, id: int, ingredients: list[tuple[int, int]], **kwargs) -> Recipe | None:
        with session_scope() as session:
            recipe_query = session.query(Recipe).filter_by(id=id)
            recipe = recipe_query.first()
            if recipe:
                recipe_query.update(kwargs)
                session.query(RecipeIngredient).filter_by(recipe_id=id).delete()
                self._add_recipe_ingredients(recipe, ingredients, session)
                return recipe
            return None

    def delete(self, id: int) -> bool:
        with session_scope() as session:
            recipe = session.query(Recipe).filter_by(id=id).first()
            if recipe:
                session.delete(recipe)
                return True
            return False

    def list_ingredients(self, search: str) -> list[Ingredient]:
        with session_scope() as session:
            return session.query(Ingredient).filter(Ingredient.name.ilike(f'%{search}%')).all()

    def _add_recipe_ingredients(self, recipe: Recipe, ingredients: list[tuple[int, int]], session: Session):
        for ingredient_id, quantity in ingredients:
            ingredient = session.query(Ingredient).filter_by(id=ingredient_id).first()
            if ingredient is None: continue
            recipe_ingredient = RecipeIngredient(recipe=recipe, ingredient=ingredient, quantity=quantity)
            session.add(recipe_ingredient)
