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

    # Edit recipe by id and dict of changes
    def update(self, id: int, ingredients: List[Tuple[int, int]], **kwargs) -> Recipe | None:
        with session_scope() as session:
            recipe_query = session.query(Recipe).filter_by(id=id)
            recipe = recipe_query.first()
            if recipe:
                recipe_query.update(kwargs)
                session.query(RecipeIngredient).filter_by(recipe_id=id).delete()
                for ingredient_id, quantity in ingredients:
                    ingredient = session.query(Ingredient).filter_by(id=ingredient_id).first()
                    recipe_ingredient = RecipeIngredient(recipe=recipe, ingredient=ingredient, quantity=quantity)
                    session.add(recipe_ingredient)
                return recipe
            return None

    def delete(self, id: int) -> bool:
        with session_scope() as session:
            recipe = session.query(Recipe).filter_by(id=id).first()
            if recipe:
                session.delete(recipe)
                return True
            return False

    #Search ingredient by name or letters
    def list_ingredients(self, search: str) -> List[Ingredient]:
        with session_scope() as session:
            return session.query(Ingredient).filter(Ingredient.name.ilike(f'%{search}%')).all()
